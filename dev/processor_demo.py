"""
Demonstration script showing how to use the Unreal Python Processor skill
with the existing Unreal Engine Python scripts in this directory.
"""

import json
from unreal_python_processor import UnrealPythonProcessor

def demo_analysis():
    """Demonstrate code analysis functionality."""
    processor = UnrealPythonProcessor()

    print("=== Unreal Python Processor Demo ===\n")

    # Analyze existing camera script
    print("1. Analyzing add_dji_camera.py...")
    with open('add_dji_camera.py', 'r', encoding='utf-8') as f:
        camera_code = f.read()

    analysis = processor.analyze_code(camera_code)
    print(f"   Found {len(analysis['functions']['functions'])} functions")
    print(f"   Complexity score: {analysis['complexity']['cyclomatic_complexity']}")
    print(f"   Code quality score: {analysis['code_quality']['score']}")

    # Show Unreal API usage
    print("   Unreal APIs used:")
    for category, apis in analysis['unreal_apis'].items():
        if apis:
            print(f"     - {category}: {', '.join(apis)}")

    print()

def demo_validation():
    """Demonstrate code validation functionality."""
    processor = UnrealPythonProcessor()

    print("2. Validating remove_unused_material_slots.py...")
    with open('remove_unused_material_slots.py', 'r', encoding='utf-8') as f:
        material_code = f.read()

    validation = processor.validate_code(material_code)

    if validation['is_valid']:
        print("   ✅ Code is valid")
    else:
        print("   ❌ Code has issues:")
        for error in validation['errors']:
            print(f"     - {error}")

    if validation['warnings']:
        print("   ⚠️ Warnings:")
        for warning in validation['warnings']:
            print(f"     - {warning}")

    print()

def demo_templates():
    """Demonstrate code template generation."""
    processor = UnrealPythonProcessor()

    print("3. Generating code templates...")

    # Generate actor manager template
    print("   Generating actor manager template...")
    actor_template = processor.generate_code_template('actor_manager')
    with open('generated_actor_manager.py', 'w', encoding='utf-8') as f:
        f.write(actor_template)
    print("   ✅ Saved to generated_actor_manager.py")

    # Generate material processor template
    print("   Generating material processor template...")
    material_template = processor.generate_code_template('material_processor')
    with open('generated_material_processor.py', 'w', encoding='utf-8') as f:
        f.write(material_template)
    print("   ✅ Saved to generated_material_processor.py")

    print()

def demo_directory_analysis():
    """Demonstrate directory-wide analysis."""
    processor = UnrealPythonProcessor()

    print("4. Analyzing entire directory...")
    results = processor.process_directory('.', 'analyze')

    print(f"   Analyzed {len(results)} Python files:")
    for file_path, result in results.items():
        if 'error' not in result:
            func_count = len(result['functions']['functions'])
            complexity = result['complexity']['cyclomatic_complexity']
            print(f"     - {file_path}: {func_count} functions, complexity {complexity}")
        else:
            print(f"     - {file_path}: Error - {result['error']}")

    # Save detailed results
    with open('directory_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("   ✅ Detailed results saved to directory_analysis.json")

    print()

def demo_optimization():
    """Demonstrate code optimization."""
    processor = UnrealPythonProcessor()

    print("5. Demonstrating code optimization...")

    # Create a sample code with optimization opportunities
    sample_code = '''
import unreal

def process_actors():
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    result = []
    for actor in actors:
        if actor.get_actor_label().startswith("Camera"):
            result.append(actor.get_actor_label())
    return result

def process_actors_again():
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    result = []
    for actor in actors:
        if actor.get_actor_label().startswith("Light"):
            result.append(actor.get_actor_label())
    return result
'''

    print("   Original code:")
    print(sample_code)

    optimization = processor.optimize_code(sample_code, 'standard')

    if 'error' not in optimization:
        print("   Optimized code:")
        print(optimization['optimized_code'])
        print(f"   Changes made: {', '.join(optimization['changes'])}")
    else:
        print(f"   Optimization failed: {optimization['error']}")

    print()

def create_enhanced_scripts():
    """Create enhanced versions of existing scripts using the processor."""
    print("6. Creating enhanced scripts...")

    # Enhanced actor info script
    enhanced_actor_info = '''import unreal
import csv
from typing import List, Dict, Optional
from unreal_python_processor import UnrealPythonProcessor

class EnhancedActorInfoExtractor:
    """Enhanced actor information extractor with validation and error handling."""

    def __init__(self):
        self.editor_level_lib = unreal.EditorLevelLibrary()
        self.processor = UnrealPythonProcessor()

    def validate_actors(self, actors: List[unreal.Actor]) -> Dict[str, List]:
        """Validate actors before processing."""
        validation_result = {
            'valid': [],
            'invalid': [],
            'warnings': []
        }

        for actor in actors:
            try:
                # Basic validation
                if not actor.get_actor_label():
                    validation_result['invalid'].append({
                        'actor': actor,
                        'reason': 'No actor label'
                    })
                    continue

                # Check for required properties
                if hasattr(actor, 'get_folder_path'):
                    try:
                        folder_path = actor.get_folder_path()
                        if not folder_path:
                            validation_result['warnings'].append({
                                'actor': actor,
                                'warning': 'No folder path'
                            })
                    except:
                        validation_result['warnings'].append({
                            'actor': actor,
                            'warning': 'Could not get folder path'
                        })

                validation_result['valid'].append(actor)

            except Exception as e:
                validation_result['invalid'].append({
                    'actor': actor,
                    'reason': f'Validation error: {str(e)}'
                })

        return validation_result

    def extract_actor_info(self, selected_only: bool = True) -> List[Dict]:
        """Extract actor information with enhanced error handling."""
        if selected_only:
            actors = self.editor_level_lib.get_selected_level_actors()
        else:
            actors = self.editor_level_lib.get_all_level_actors()

        # Validate actors first
        validation_result = self.validate_actors(actors)

        # Log validation results
        if validation_result['invalid']:
            unreal.log_warning(f"Found {len(validation_result['invalid'])} invalid actors")

        if validation_result['warnings']:
            unreal.log_warning(f"Found {len(validation_result['warnings'])} actors with warnings")

        # Process valid actors
        actor_info_list = []

        for actor in validation_result['valid']:
            try:
                actor_info = {
                    'name': actor.get_actor_label(),
                    'class': actor.__class__.__name__,
                    'eid': self._extract_eid_from_tags(actor),
                    'folder_path': self._safe_get_folder_path(actor),
                    'location': actor.get_actor_location(),
                    'rotation': actor.get_actor_rotation(),
                    'tags': list(actor.tags)
                }
                actor_info_list.append(actor_info)

            except Exception as e:
                unreal.log_error(f"Error processing actor {actor.get_actor_label()}: {str(e)}")
                continue

        return actor_info_list

    def _extract_eid_from_tags(self, actor: unreal.Actor) -> Optional[str]:
        """Extract EID from actor tags."""
        try:
            for tag in actor.tags:
                str_tag = str(tag)
                if "EID=" in str_tag:
                    return str_tag.replace("EID=", "")
            return None
        except Exception:
            return None

    def _safe_get_folder_path(self, actor: unreal.Actor) -> str:
        """Safely get folder path."""
        try:
            folder_path = actor.get_folder_path()
            return str(folder_path) if folder_path else "None"
        except Exception:
            return "Unknown"

    def export_to_csv(self, actor_info_list: List[Dict], file_path: str) -> bool:
        """Export actor information to CSV with enhanced error handling."""
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                if not actor_info_list:
                    unreal.log_warning("No actor information to export")
                    return False

                fieldnames = ['EID', 'Type', 'Name', 'Folder_Path', 'Location_X', 'Location_Y', 'Location_Z', 'Tags']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for actor_info in actor_info_list:
                    writer.writerow({
                        'EID': actor_info.get('eid', ''),
                        'Type': actor_info.get('class', ''),
                        'Name': actor_info.get('name', ''),
                        'Folder_Path': actor_info.get('folder_path', ''),
                        'Location_X': actor_info.get('location', unreal.Vector(0,0,0)).x,
                        'Location_Y': actor_info.get('location', unreal.Vector(0,0,0)).y,
                        'Location_Z': actor_info.get('location', unreal.Vector(0,0,0)).z,
                        'Tags': '; '.join(actor_info.get('tags', []))
                    })

            unreal.log(f"Successfully exported {len(actor_info_list)} actors to {file_path}")
            return True

        except Exception as e:
            unreal.log_error(f"Failed to export to CSV: {str(e)}")
            return False

# Usage
if __name__ == "__main__":
    extractor = EnhancedActorInfoExtractor()
    actor_info = extractor.extract_actor_info(selected_only=False)
    success = extractor.export_to_csv(actor_info, "enhanced_actor_info.csv")

    if success:
        print(f"Exported {len(actor_info)} actors to enhanced_actor_info.csv")
    else:
        print("Export failed")
'''

    with open('enhanced_actor_info_extractor.py', 'w', encoding='utf-8') as f:
        f.write(enhanced_actor_info)
    print("   ✅ Created enhanced_actor_info_extractor.py")

    print()

def main():
    """Run all demonstrations."""
    try:
        demo_analysis()
        demo_validation()
        demo_templates()
        demo_directory_analysis()
        demo_optimization()
        create_enhanced_scripts()

        print("=== Demo Complete ===")
        print("The Unreal Python Processor skill has been demonstrated with the following outputs:")
        print("- directory_analysis.json: Detailed analysis of all Python files")
        print("- generated_actor_manager.py: Actor management template")
        print("- generated_material_processor.py: Material processing template")
        print("- enhanced_actor_info_extractor.py: Enhanced version of actor info script")
        print("\nYou can now use the processor class in your own scripts!")

    except Exception as e:
        print(f"Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()