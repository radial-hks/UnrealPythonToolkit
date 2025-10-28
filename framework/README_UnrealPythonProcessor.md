# Unreal Engine Python Code Processing Skill

A comprehensive Python skill for processing, analyzing, validating, and optimizing Python code designed for Unreal Engine automation tasks.

## Features

### 🔍 Code Analysis
- **Import Analysis**: Identifies and categorizes imports (standard, third-party, local)
- **Unreal API Detection**: Recognizes usage patterns for different Unreal Engine APIs
- **Function Analysis**: Analyzes function definitions, complexity, and documentation
- **Variable Analysis**: Tracks variable declarations and constants
- **Complexity Metrics**: Calculates cyclomatic complexity and other quality metrics
- **Safety Checks**: Identifies potential safety issues and security concerns
- **Optimization Suggestions**: Provides recommendations for performance improvements

### ✅ Code Validation
- **Syntax Validation**: Checks for Python syntax errors
- **Import Validation**: Ensures required imports are present
- **Safety Validation**: Identifies potential runtime issues
- **Best Practices**: Validates against Unreal Engine Python best practices
- **Security Checks**: Scans for potential security vulnerabilities

### ⚡ Code Optimization
- **Import Optimization**: Reorganizes and optimizes import statements
- **Function Call Caching**: Identifies and optimizes repeated function calls
- **Loop Optimization**: Improves loop performance patterns
- **Variable Access Optimization**: Optimizes variable access patterns

### 📝 Code Generation
- **Template Generation**: Creates ready-to-use templates for common tasks:
  - Actor Manager
  - Material Processor
  - Camera Setup
  - Asset Batch Processor
  - Scene Analyzer

### 📁 Directory Processing
- **Batch Processing**: Analyzes all Python files in a directory
- **Comprehensive Reports**: Generates detailed analysis reports
- **JSON Export**: Exports results in structured JSON format

## Installation

1. Copy `unreal_python_processor.py` to your project directory
2. Install required dependencies:
   ```bash
   pip install astor  # For code generation
   ```

## Quick Start

### Basic Usage

```python
from unreal_python_processor import UnrealPythonProcessor

# Initialize the processor
processor = UnrealPythonProcessor()

# Analyze existing code
with open('your_script.py', 'r') as f:
    code = f.read()

analysis = processor.analyze_code(code)
print(f"Found {len(analysis['functions']['functions'])} functions")
print(f"Code quality score: {analysis['code_quality']['score']}")
```

### Validate Code

```python
validation = processor.validate_code(code)

if validation['is_valid']:
    print("✅ Code is valid")
else:
    print("❌ Issues found:")
    for error in validation['errors']:
        print(f"  - {error}")
```

### Generate Templates

```python
# Generate actor manager template
actor_template = processor.generate_code_template('actor_manager')

# Generate material processor template
material_template = processor.generate_code_template('material_processor')

# Save to file
with open('my_actor_manager.py', 'w') as f:
    f.write(actor_template)
```

### Process Entire Directory

```python
# Analyze all Python files in current directory
results = processor.process_directory('.', 'analyze')

for file_path, result in results.items():
    if 'error' not in result:
        print(f"{file_path}: {result['functions']['total_count']} functions")
```

## Command Line Interface

The skill includes a command-line interface for easy use:

```bash
# Analyze a single file
python unreal_python_processor.py analyze --file your_script.py

# Validate code
python unreal_python_processor.py validate --file your_script.py

# Optimize code
python unreal_python_processor.py optimize --file your_script.py --output optimized.py

# Generate template
python unreal_python_processor.py template --template-type actor_manager --output actor_manager.py

# Process entire directory
python unreal_python_processor.py analyze --directory ./scripts --output analysis.json
```

## Available Templates

### 1. Actor Manager (`actor_manager`)
Provides utilities for managing Unreal Engine actors:
- Get actors by name patterns
- Spawn actors at specific locations
- Delete multiple actors

### 2. Material Processor (`material_processor`)
Tools for material management:
- Get material slot information
- Remove unused materials
- Replace materials safely

### 3. Camera Setup (`camera_setup`)
Camera configuration utilities:
- Create cine cameras with custom settings
- Set filmback properties
- Configure focal lengths

### 4. Asset Batch Processor (`asset_batch_processor`)
Batch processing tools:
- Process multiple assets simultaneously
- Apply functions to selected assets
- Save multiple assets efficiently

### 5. Scene Analyzer (`scene_analyzer`)
Scene analysis tools:
- Analyze all actors in a level
- Categorize actors by class
- Export actor information to CSV

## Integration with Your Existing Scripts

The skill is designed to work seamlessly with your existing Unreal Engine Python scripts. Based on the scripts in your directory:

### Camera Scripts
Enhance scripts like `add_dji_camera.py` with:
- Error handling and validation
- Configuration management
- Reusable camera setup functions

### Material Scripts
Improve scripts like `remove_unused_material_slots.py` with:
- Better error handling
- Performance optimizations
- Enhanced safety checks

### Actor Information Scripts
Upgrade scripts like `get_actor_name.py` with:
- Structured data extraction
- CSV export capabilities
- Validation and error handling

## Example: Enhanced Actor Information Script

```python
from unreal_python_processor import UnrealPythonProcessor
import unreal
import csv

class EnhancedActorInfoExtractor:
    def __init__(self):
        self.processor = UnrealPythonProcessor()
        self.editor_level_lib = unreal.EditorLevelLibrary()

    def extract_and_export(self, file_path: str):
        """Extract actor information and export to CSV."""
        actors = self.editor_level_lib.get_all_level_actors()

        # Enhanced processing with validation
        processed_actors = []
        for actor in actors:
            try:
                actor_info = {
                    'name': actor.get_actor_label(),
                    'eid': self._extract_eid(actor),
                    'folder_path': str(actor.get_folder_path()),
                    'class': actor.__class__.__name__
                }
                processed_actors.append(actor_info)
            except Exception as e:
                unreal.log_warning(f"Failed to process {actor.get_name()}: {e}")

        # Export to CSV
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'eid', 'folder_path', 'class'])
            writer.writeheader()
            writer.writerows(processed_actors)

        unreal.log(f"Exported {len(processed_actors)} actors to {file_path}")

    def _extract_eid(self, actor):
        """Extract EID from actor tags."""
        for tag in actor.tags:
            if "EID=" in str(tag):
                return str(tag).replace("EID=", "")
        return None

# Usage
extractor = EnhancedActorInfoExtractor()
extractor.extract_and_export("enhanced_actor_info.csv")
```

## Best Practices

When using this skill with Unreal Engine Python scripts:

1. **Always Include Error Handling**: Unreal Engine operations can fail
2. **Use Proper Logging**: Log information, warnings, and errors appropriately
3. **Validate Assets**: Check if assets exist before processing
4. **Handle Edge Cases**: Consider null values, missing properties
5. **Optimize Performance**: Cache expensive operations
6. **Document Your Code**: Include docstrings for functions

## Files Created for You

The skill creation process generated these files:

1. **`unreal_python_processor.py`** - The main skill module
2. **`demo_processor_usage.py`** - Demonstration script showing usage
3. **`README_UnrealPythonProcessor.md`** - This documentation
4. **Template files** (generated when using template generation)

## Next Steps

1. Explore the demo script to understand usage patterns
2. Try analyzing your existing scripts
3. Generate templates for new functionality
4. Integrate the processor into your workflow
5. Extend the skill with custom functionality

## Technical Details

- **Compatible with**: Python 3.7+
- **Unreal Engine**: 4.27+ (tested with UE5)
- **Dependencies**: `astor` (for code generation)
- **AST-based**: Uses Python Abstract Syntax Tree for analysis
- **Extensible**: Easy to add new analysis rules and templates

## Contributing

To extend the skill:

1. Add new API patterns to `unreal_api_patterns`
2. Create new templates in the `_generate_*_template` methods
3. Add new validation rules in the `_validate_*` methods
4. Implement new optimization strategies in the `CodeOptimizer` class

## License

This skill is provided as-is for educational and development purposes. Use it according to your project requirements and Unreal Engine licensing terms.