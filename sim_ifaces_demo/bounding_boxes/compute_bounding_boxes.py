#!/usr/bin/env python3

import os
import tempfile
from urllib.parse import urlparse
import sys

# Gazebo API imports
from gz.sim import (TestFixture, Link, Model, K_NULL_ENTITY, World,
                     world_entity)
from gz.math import AxisAlignedBox

def get_model_name_from_uri(uri: str) -> str:
    """Extracts a model name from a Gazebo Fuel URI."""
    try:
        path = urlparse(uri).path
        model_name = os.path.basename(path)
        if not model_name:
            raise ValueError("Could not parse model name from URI")
        return model_name
    except Exception as e:
        print(f"Error: Invalid model URI provided: {uri}. {e}", file=sys.stderr)
        return ""

def generate_world_sdf(model_uris: list) -> str:
    """
    Generates a single world SDF string that includes all specified models,
    spaced out to prevent initial collisions.
    """
    include_tags = []
    # Space models 1 meters apart along the x-axis.
    spacing = 1.0
    for i, uri in enumerate(model_uris):
        model_name = get_model_name_from_uri(uri)
        if model_name:
            pose = f"{i * spacing} 0 0 0 0 0"
            include_tags.append(f"""
            <include>
              <name>{model_name}</name>
              <uri>{uri}</uri>
              <pose>{pose}</pose>
            </include>""")

    return f"""
    <sdf version='1.7'>
      <world name='bounding_box_world'>
        {''.join(include_tags)}
      </world>
    </sdf>
    """

def main():
    """
    Main function to calculate and print bounding boxes for a list of models.
    """
    model_uris = [
        "https://fuel.gazebosim.org/1.0/GoogleResearch/models/Weisshai_Great_White_Shark",
        "https://fuel.gazebosim.org/1.0/GoogleResearch/models/Vtech_Roll_Learn_Turtle",
        "https://fuel.gazebosim.org/1.0/GoogleResearch/models/Sootheze_Toasty_Orca",
        "https://fuel.gazebosim.org/1.0/GoogleResearch/models/Dino_3",
        "https://fuel.gazebosim.org/1.0/GoogleResearch/models/Dino_4",
    ]

    model_names = [get_model_name_from_uri(uri) for uri in model_uris if uri]

    world_sdf_string = generate_world_sdf(model_uris)
    print(world_sdf_string)

    world_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.sdf', encoding='utf-8'
        ) as f:
            f.write(world_sdf_string)
            world_file = f.name

        fixture = TestFixture(world_file)

        results = {}
        iteration_count = 0
        setup_complete = False

        def on_pre_update(info, ecm):
            """
            Enable bounding box checks for all links on all models.
            This only needs to run once after the models are spawned.
            """
            nonlocal setup_complete
            if setup_complete:
                return

            world_entity_val = world_entity(ecm)
            if world_entity_val == K_NULL_ENTITY:
                return

            world = World(world_entity_val)
            
            # Wait until all expected models are loaded into the simulation.
            if world.model_count(ecm) < len(model_names):
                return

            model_entities = world.models(ecm)
            for model_entity in model_entities:
                model = Model(model_entity)
                if not model.valid(ecm):
                    continue
                for link_entity in model.links(ecm):
                    link = Link(link_entity)
                    if link.valid(ecm):
                        link.enable_bounding_box_checks(ecm, True)
            
            setup_complete = True

        def on_post_update(info, ecm):
            """
            After physics has run, read the final world-axis-aligned bounding box.
            """
            nonlocal iteration_count

            if not setup_complete:
                return

            # Stop once we've found all models or after a timeout.
            if len(results) == len(model_names) or iteration_count > 50:
                return
            iteration_count += 1

            world_entity_val = world_entity(ecm)
            if world_entity_val == K_NULL_ENTITY:
                return
            world = World(world_entity_val)

            for model_entity in world.models(ecm):
                model = Model(model_entity)
                if not model.valid(ecm):
                    continue
                
                model_name = model.name(ecm)

                if model_name in results or model_name not in model_names:
                    continue

                combined_box = AxisAlignedBox()
                found_at_least_one_link = False

                for link_entity in model.links(ecm):
                    link = Link(link_entity)
                    if link.valid(ecm):
                        link_box = link.world_axis_aligned_box(ecm)
                        if link_box and (link_box.volume() > 1e-9 or link_box.min() != link_box.max()):
                            if not found_at_least_one_link:
                                combined_box = link_box
                            else:
                                combined_box += link_box
                            found_at_least_one_link = True
                
                if found_at_least_one_link:
                    results[model_name] = combined_box

        fixture.on_pre_update(on_pre_update)
        fixture.on_post_update(on_post_update)
        fixture.finalize()
        fixture.server().run(True, 60, False)

        # Print results
        print("--- Bounding Box Calculation Results ---")
        for name in model_names:
            print(f"\nModel: {name}")
            if name in results:
                bbox = results[name]
                print(f"  -> Bounding Box Min: {bbox.min()}")
                print(f"  -> Bounding Box Max: {bbox.max()}")
                print(f"  -> Bounding Box Center: {bbox.center()}")
                print(f"  -> Bounding Box Size: {bbox.size()}")
            else:
                print("  -> Failed to determine bounding box.")

    finally:
        if world_file and os.path.exists(world_file):
            os.remove(world_file)

if __name__ == '__main__':
    os.environ['GZ_LOG_LEVEL'] = '3'
    main()

