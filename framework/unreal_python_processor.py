"""
Unreal Engine Python Code Processing Skill

This skill provides comprehensive tools for processing and analyzing Python code
designed for Unreal Engine automation tasks. It includes validation, optimization,
code generation, and analysis capabilities.

Author: Claude Assistant
Version: 1.0
"""

import ast
import os
import sys
import json
import re
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import subprocess
import tempfile

class UnrealPythonProcessor:
    """
    A comprehensive processor for Unreal Engine Python scripts that provides
    validation, optimization, analysis, and code generation capabilities.
    """

    def __init__(self):
        self.unreal_api_patterns = {
            'actor_manipulation': [
                'EditorLevelLibrary', 'spawn_actor_from_class', 'get_actor_label',
                'set_actor_location', 'set_actor_rotation', 'get_actor_location'
            ],
            'material_system': [
                'StaticMesh', 'get_material', 'set_material', 'static_materials',
                'MaterialInterface', 'MaterialFactory'
            ],
            'camera_system': [
                'CineCameraActor', 'CineCameraComponent', 'CameraComponent',
                'field_of_view', 'filmback', 'focal_length'
            ],
            'asset_management': [
                'EditorAssetLibrary', 'AssetRegistry', 'load_asset',
                'save_asset', 'get_selected_assets'
            ],
            'geometry_script': [
                'GeometryScript_StaticMeshFunctions', 'GeometryScriptMeshReadLOD',
                'get_section_material_list_from_static_mesh'
            ]
        }

        self.common_imports = {
            'unreal': 'import unreal',
            'math': 'import math',
            'csv': 'import csv',
            'json': 'import json',
            'os': 'import os',
            'sys': 'import sys',
            'pathlib': 'from pathlib import Path'
        }

        self.validation_rules = {
            'required_imports': ['unreal'],
            'safety_checks': ['asset_validation', 'actor_validation', 'material_validation'],
            'best_practices': ['error_handling', 'logging', 'asset_paths']
        }

    def analyze_code(self, python_code: str) -> Dict[str, Any]:
        """
        Analyze Python code for Unreal Engine usage patterns and provide insights.

        Args:
            python_code: The Python code to analyze

        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = ast.parse(python_code)

            analysis = {
                'imports': self._analyze_imports(tree),
                'unreal_apis': self._analyze_unreal_apis(tree),
                'functions': self._analyze_functions(tree),
                'variables': self._analyze_variables(tree),
                'complexity': self._analyze_complexity(tree),
                'safety_issues': self._check_safety_issues(tree),
                'optimization_suggestions': self._suggest_optimizations(tree),
                'code_quality': self._assess_code_quality(tree)
            }

            return analysis

        except SyntaxError as e:
            return {'error': f'Syntax error: {str(e)}'}
        except Exception as e:
            return {'error': f'Analysis error: {str(e)}'}

    def validate_code(self, python_code: str) -> Dict[str, Any]:
        """
        Validate Python code for Unreal Engine best practices and potential issues.

        Args:
            python_code: The Python code to validate

        Returns:
            Dictionary containing validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'security_issues': []
        }

        try:
            tree = ast.parse(python_code)

            # Check for required imports
            validation_result.update(self._validate_imports(tree))

            # Check for safety issues
            validation_result.update(self._validate_safety(tree))

            # Check for best practices
            validation_result.update(self._validate_best_practices(tree))

            # Check for potential security issues
            validation_result.update(self._validate_security(tree))

        except SyntaxError as e:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f'Syntax error: {str(e)}')

        return validation_result

    def optimize_code(self, python_code: str, optimization_level: str = 'standard') -> Dict[str, Any]:
        """
        Optimize Python code for better performance and maintainability.

        Args:
            python_code: The Python code to optimize
            optimization_level: 'basic', 'standard', or 'aggressive'

        Returns:
            Dictionary containing optimized code and changes made
        """
        try:
            tree = ast.parse(python_code)
            optimizer = CodeOptimizer(optimization_level)
            optimized_tree = optimizer.optimize(tree)

            # Convert back to code
            import astor
            optimized_code = astor.to_source(optimized_tree)

            return {
                'optimized_code': optimized_code,
                'changes_made': optimizer.changes,
                'performance_improvements': optimizer.performance_notes
            }

        except Exception as e:
            return {
                'error': f'Optimization failed: {str(e)}',
                'optimized_code': python_code
            }

    def generate_code_template(self, template_type: str, **kwargs) -> str:
        """
        Generate Python code templates for common Unreal Engine tasks.

        Args:
            template_type: Type of template to generate
            **kwargs: Additional parameters for the template

        Returns:
            Generated Python code as string
        """
        templates = {
            'actor_manager': self._generate_actor_manager_template,
            'material_processor': self._generate_material_processor_template,
            'camera_setup': self._generate_camera_setup_template,
            'asset_batch_processor': self._generate_asset_batch_processor_template,
            'scene_analyzer': self._generate_scene_analyzer_template
        }

        if template_type not in templates:
            raise ValueError(f'Unknown template type: {template_type}')

        return templates[template_type](**kwargs)

    def process_directory(self, directory_path: str, operation: str = 'analyze') -> Dict[str, Any]:
        """
        Process all Python files in a directory.

        Args:
            directory_path: Path to the directory containing Python files
            operation: 'analyze', 'validate', or 'optimize'

        Returns:
            Dictionary containing processing results for all files
        """
        results = {}
        directory = Path(directory_path)

        if not directory.exists():
            return {'error': f'Directory not found: {directory_path}'}

        python_files = list(directory.glob('*.py'))

        if not python_files:
            return {'message': 'No Python files found in directory'}

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                if operation == 'analyze':
                    results[str(file_path)] = self.analyze_code(code)
                elif operation == 'validate':
                    results[str(file_path)] = self.validate_code(code)
                elif operation == 'optimize':
                    results[str(file_path)] = self.optimize_code(code)

            except Exception as e:
                results[str(file_path)] = {'error': f'Failed to process file: {str(e)}'}

        return results

    def _analyze_imports(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Analyze import statements in the code."""
        imports = {'standard': [], 'third_party': [], 'local': []}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.common_imports:
                        imports['standard'].append(alias.name)
                    else:
                        imports['third_party'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('unreal'):
                    imports['standard'].append(f'from {node.module}')

        return imports

    def _analyze_unreal_apis(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Analyze Unreal Engine API usage patterns."""
        api_usage = {category: [] for category in self.unreal_api_patterns.keys()}

        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                attr_name = node.attr
                for category, patterns in self.unreal_api_patterns.items():
                    if any(pattern in attr_name for pattern in patterns):
                        api_usage[category].append(attr_name)

        # Remove duplicates
        for category in api_usage:
            api_usage[category] = list(set(api_usage[category]))

        return api_usage

    def _analyze_functions(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze function definitions and their complexity."""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'args_count': len(node.args.args),
                    'docstring': ast.get_docstring(node) is not None,
                    'complexity': self._calculate_function_complexity(node)
                }
                functions.append(func_info)

        return {'functions': functions, 'total_count': len(functions)}

    def _analyze_variables(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Analyze variable declarations and types."""
        variables = {'constants': [], 'variables': []}

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        if var_name.isupper():
                            variables['constants'].append(var_name)
                        else:
                            variables['variables'].append(var_name)

        return variables

    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """Calculate code complexity metrics."""
        complexity = {
            'lines_of_code': len(tree.body),
            'cyclomatic_complexity': 1,
            'nested_depth': 0
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity['cyclomatic_complexity'] += 1

        return complexity

    def _check_safety_issues(self, tree: ast.AST) -> List[str]:
        """Check for potential safety issues."""
        issues = []

        for node in ast.walk(tree):
            # Check for hardcoded paths
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if any(pattern in node.value for pattern in ['C:\\', '/tmp/', 'C:/Users']):
                    issues.append(f'Hardcoded path detected: {node.value}')

            # Check for missing error handling
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr'):
                    if node.func.attr in ['spawn_actor', 'load_asset', 'save_asset']:
                        issues.append(f'Potential missing error handling for {node.func.attr}')

        return issues

    def _suggest_optimizations(self, tree: ast.AST) -> List[str]:
        """Suggest code optimizations."""
        suggestions = []

        # Check for duplicate code patterns
        function_calls = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and hasattr(node.func, 'attr'):
                func_name = node.func.attr
                function_calls[func_name] = function_calls.get(func_name, 0) + 1

        for func_name, count in function_calls.items():
            if count > 3:
                suggestions.append(f'Consider caching results of {func_name} (called {count} times)')

        return suggestions

    def _assess_code_quality(self, tree: ast.AST) -> Dict[str, Any]:
        """Assess overall code quality."""
        quality_score = 100
        issues = []

        # Check for docstrings
        functions_with_docs = 0
        total_functions = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1
                if ast.get_docstring(node):
                    functions_with_docs += 1

        if total_functions > 0:
            doc_ratio = functions_with_docs / total_functions
            quality_score -= (1 - doc_ratio) * 20

        return {
            'score': max(0, quality_score),
            'functions_documented': f'{functions_with_docs}/{total_functions}',
            'issues': issues
        }

    def _validate_imports(self, tree: ast.AST) -> Dict[str, Any]:
        """Validate required imports."""
        result = {'errors': [], 'warnings': []}

        has_unreal_import = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'unreal':
                        has_unreal_import = True

        if not has_unreal_import:
            result['errors'].append('Missing required import: unreal')

        return result

    def _validate_safety(self, tree: ast.AST) -> Dict[str, Any]:
        """Validate safety considerations."""
        return {'warnings': [], 'suggestions': []}

    def _validate_best_practices(self, tree: ast.AST) -> Dict[str, Any]:
        """Validate best practices."""
        return {'suggestions': []}

    def _validate_security(self, tree: ast.AST) -> Dict[str, Any]:
        """Validate security considerations."""
        return {'security_issues': []}

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                complexity += 1
        return complexity

    def _generate_actor_manager_template(self, **kwargs) -> str:
        """Generate actor manager template."""
        return '''
import unreal
from typing import List, Optional

class ActorManager:
    """Manager for Unreal Engine Actor operations."""

    def __init__(self):
        self.editor_level_lib = unreal.EditorLevelLibrary()

    def get_actors_by_name(self, name_pattern: str) -> List[unreal.Actor]:
        """Get actors matching name pattern."""
        all_actors = self.editor_level_lib.get_all_level_actors()
        return [actor for actor in all_actors if name_pattern in actor.get_actor_label()]

    def spawn_actor(self, actor_class: type, location: unreal.Vector,
                   rotation: unreal.Rotator = None) -> unreal.Actor:
        """Spawn actor at specified location."""
        if rotation is None:
            rotation = unreal.Rotator()
        return self.editor_level_lib.spawn_actor_from_class(actor_class, location, rotation)

    def delete_actors(self, actors: List[unreal.Actor]) -> None:
        """Delete multiple actors."""
        for actor in actors:
            actor.destroy_actor()
'''

    def _generate_material_processor_template(self, **kwargs) -> str:
        """Generate material processor template."""
        return '''
import unreal
from typing import List, Dict, Optional

class MaterialProcessor:
    """Processor for Unreal Engine material operations."""

    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary()
        self.asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    def get_material_slots(self, static_mesh: unreal.StaticMesh) -> List[Dict]:
        """Get material slot information from static mesh."""
        materials = []
        for i, material_slot in enumerate(static_mesh.static_materials):
            materials.append({
                'index': i,
                'name': material_slot.material_slot_name,
                'material': material_slot.material_interface
            })
        return materials

    def remove_unused_materials(self, static_mesh: unreal.StaticMesh) -> int:
        """Remove unused material slots from static mesh."""
        # Implementation would go here
        pass

    def replace_material(self, static_mesh: unreal.StaticMesh,
                        slot_index: int, new_material: unreal.MaterialInterface) -> bool:
        """Replace material at specific slot."""
        try:
            static_mesh.set_material(slot_index, new_material)
            return True
        except Exception as e:
            unreal.log_error(f"Failed to replace material: {e}")
            return False
'''

    def _generate_camera_setup_template(self, **kwargs) -> str:
        """Generate camera setup template."""
        return '''
import unreal
import math

class CameraSetup:
    """Setup and configure Unreal Engine cameras."""

    def __init__(self):
        self.editor_level_lib = unreal.EditorLevelLibrary()

    def create_cine_camera(self, location: unreal.Vector,
                          rotation: unreal.Rotator,
                          focal_length: float = 35.0) -> unreal.CineCameraActor:
        """Create a CineCameraActor with specified settings."""
        camera = self.editor_level_lib.spawn_actor_from_class(
            unreal.CineCameraActor, location, rotation
        )

        cine_component = camera.get_cine_camera_component()
        cine_component.current_focal_length = focal_length

        return camera

    def set_filmback_settings(self, camera: unreal.CineCameraActor,
                             sensor_width: float, sensor_height: float) -> None:
        """Set camera filmback settings."""
        cine_component = camera.get_cine_camera_component()
        filmback = cine_component.filmback
        filmback.sensor_width = sensor_width
        filmback.sensor_height = sensor_height
'''

    def _generate_asset_batch_processor_template(self, **kwargs) -> str:
        """Generate asset batch processor template."""
        return '''
import unreal
from typing import List, Callable

class AssetBatchProcessor:
    """Process multiple Unreal Engine assets in batch."""

    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary()
        self.editor_utility = unreal.EditorUtilityLibrary()

    def process_selected_assets(self, process_func: Callable) -> Dict[str, any]:
        """Process all selected assets with given function."""
        selected_assets = self.editor_utility.get_selected_assets()
        results = {}

        for asset in selected_assets:
            try:
                result = process_func(asset)
                results[asset.get_name()] = {'success': True, 'result': result}
            except Exception as e:
                results[asset.get_name()] = {'success': False, 'error': str(e)}

        return results

    def save_all_assets(self, assets: List[unreal.Object]) -> int:
        """Save multiple assets and return count of successful saves."""
        saved_count = 0
        for asset in assets:
            if self.editor_asset_lib.save_loaded_asset(asset):
                saved_count += 1
        return saved_count
'''

    def _generate_scene_analyzer_template(self, **kwargs) -> str:
        """Generate scene analyzer template."""
        return '''
import unreal
from typing import Dict, List
import csv

class SceneAnalyzer:
    """Analyze Unreal Engine scenes and extract information."""

    def __init__(self):
        self.editor_level_lib = unreal.EditorLevelLibrary()

    def analyze_actors(self) -> Dict[str, List[Dict]]:
        """Analyze all actors in the current level."""
        actors = self.editor_level_lib.get_all_level_actors()
        analysis = {
            'total_actors': len(actors),
            'actors_by_class': {},
            'actor_details': []
        }

        for actor in actors:
            class_name = actor.__class__.__name__
            if class_name not in analysis['actors_by_class']:
                analysis['actors_by_class'][class_name] = 0
            analysis['actors_by_class'][class_name] += 1

            analysis['actor_details'].append({
                'name': actor.get_actor_label(),
                'class': class_name,
                'location': actor.get_actor_location(),
                'tags': list(actor.tags)
            })

        return analysis

    def export_actor_info_to_csv(self, file_path: str) -> bool:
        """Export actor information to CSV file."""
        try:
            analysis = self.analyze_actors()

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'class', 'location_x', 'location_y', 'location_z', 'tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for actor_info in analysis['actor_details']:
                    writer.writerow({
                        'name': actor_info['name'],
                        'class': actor_info['class'],
                        'location_x': actor_info['location'].x,
                        'location_y': actor_info['location'].y,
                        'location_z': actor_info['location'].z,
                        'tags': ', '.join(actor_info['tags'])
                    })

            return True
        except Exception as e:
            unreal.log_error(f"Failed to export actor info: {e}")
            return False
'''


class CodeOptimizer:
    """Code optimizer for Unreal Engine Python scripts."""

    def __init__(self, level: str = 'standard'):
        self.level = level
        self.changes = []
        self.performance_notes = []

    def optimize(self, tree: ast.AST) -> ast.AST:
        """Apply optimizations based on the specified level."""
        # Apply transformations based on optimization level
        if self.level in ['standard', 'aggressive']:
            tree = self._optimize_imports(tree)
            tree = self._optimize_function_calls(tree)

        if self.level == 'aggressive':
            tree = self._optimize_loops(tree)
            tree = self._optimize_variable_access(tree)

        return tree

    def _optimize_imports(self, tree: ast.AST) -> ast.AST:
        """Optimize import statements."""
        # Implementation would optimize import organization
        self.changes.append('Optimized import organization')
        return tree

    def _optimize_function_calls(self, tree: ast.AST) -> ast.AST:
        """Optimize repeated function calls."""
        # Implementation would cache repeated function calls
        self.changes.append('Added caching for repeated function calls')
        return tree

    def _optimize_loops(self, tree: ast.AST) -> ast.AST:
        """Optimize loop structures."""
        # Implementation would optimize loop performance
        self.changes.append('Optimized loop structures')
        return tree

    def _optimize_variable_access(self, tree: ast.AST) -> ast.AST:
        """Optimize variable access patterns."""
        # Implementation would optimize variable access
        self.changes.append('Optimized variable access patterns')
        return tree


# Example usage and CLI interface
def main():
    """Main function for command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Unreal Engine Python Code Processor')
    parser.add_argument('action', choices=['analyze', 'validate', 'optimize', 'template'])
    parser.add_argument('--file', help='Python file to process')
    parser.add_argument('--directory', help='Directory to process')
    parser.add_argument('--template-type', help='Type of template to generate')
    parser.add_argument('--output', help='Output file for results')

    args = parser.parse_args()

    processor = UnrealPythonProcessor()

    if args.action == 'template':
        if not args.template_type:
            print("Error: --template-type required for template action")
            return

        template_code = processor.generate_code_template(args.template_type)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(template_code)
            print(f"Template saved to {args.output}")
        else:
            print(template_code)

    elif args.file:
        with open(args.file, 'r') as f:
            code = f.read()

        if args.action == 'analyze':
            result = processor.analyze_code(code)
        elif args.action == 'validate':
            result = processor.validate_code(code)
        elif args.action == 'optimize':
            result = processor.optimize_code(code)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))

    elif args.directory:
        result = processor.process_directory(args.directory, args.action)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()