"""
Unit tests for CLI module
"""

import pytest
import sys
from pathlib import Path
from cryptic_screening.cli import (
    get_env_or_default,
    create_parser,
    load_config,
    apply_config_to_args,
)

class TestGetEnvOrDefault:
    """Test environment variable handling"""
    
    def test_get_env_string(self, monkeypatch):
        """Test getting string from environment"""
        monkeypatch.setenv("TEST_VAR", "test_value")
        assert get_env_or_default("TEST_VAR", "default") == "test_value"
    
    def test_get_env_default(self):
        """Test getting default when env var not set"""
        assert get_env_or_default("NONEXISTENT_VAR", "default") == "default"
    
    def test_get_env_int(self, monkeypatch):
        """Test getting integer from environment"""
        monkeypatch.setenv("TEST_INT", "42")
        assert get_env_or_default("TEST_INT", 10, int) == 42
    
    def test_get_env_invalid_int(self, monkeypatch, caplog):
        """Test invalid integer conversion"""
        monkeypatch.setenv("TEST_INT", "not_a_number")
        result = get_env_or_default("TEST_INT", "10", int)
        assert result == 10
        assert "Invalid value" in caplog.text

class TestCreateParser:
    """Test argument parser creation"""
    
    def test_parser_creation(self):
        """Test that parser is created successfully"""
        parser = create_parser()
        assert parser.prog == 'cryptic-screen'
    
    def test_subcommands_exist(self):
        """Test that all subcommands are present"""
        parser = create_parser()
        # Parse with no arguments to check subcommands
        with pytest.raises(SystemExit):
            parser.parse_args(['--help'])
    
    def test_nt_command_args(self):
        """Test NT command arguments"""
        parser = create_parser()
        args = parser.parse_args(['nt', '--input', '/test/dir'])
        assert args.command == 'nt'
        assert args.input == '/test/dir'
    
    def test_pm_command_args(self):
        """Test PM command arguments"""
        parser = create_parser()
        args = parser.parse_args(['pm', '--input', '/test/dir', '--total-cutoff', '5'])
        assert args.command == 'pm'
        assert args.input == '/test/dir'
        assert args.total_cutoff == 5
    
    def test_winnow_command_args(self):
        """Test winnow command arguments"""
        parser = create_parser()
        args = parser.parse_args(['winnow', '--nt-results', 'results.tsv'])
        assert args.command == 'winnow'
        assert args.nt_results == 'results.tsv'
    
    def test_derep_command_args(self, temp_dir):
        """Test derep command arguments"""
        parser = create_parser()
        input_file = temp_dir / "input.fa"
        output_file = temp_dir / "output.fa"
        input_file.write_text("test")
        
        args = parser.parse_args(['derep', str(input_file), str(output_file)])
        assert args.command == 'derep'
        assert args.input.name == str(input_file)
        assert args.output.name == str(output_file)
    
    def test_common_arguments(self):
        """Test common arguments across commands"""
        parser = create_parser()
        args = parser.parse_args([
            'nt',
            '--input', '/test',
            '--data-dir', '/data',
            '--output-dir', '/output',
            '--workers', '8',
            '--log-level', 'DEBUG',
            '--dry-run'
        ])
        assert args.data_dir == '/data'
        assert args.output_dir == '/output'
        assert args.workers == 8
        assert args.log_level == 'DEBUG'
        assert args.dry_run is True

class TestLoadConfig:
    """Test configuration file loading"""
    
    def test_load_valid_config(self, sample_config):
        """Test loading valid YAML config"""
        config = load_config(str(sample_config))
        assert 'global' in config
        assert config['global']['workers'] == 2
    
    def test_load_missing_config(self):
        """Test loading non-existent config file"""
        with pytest.raises(SystemExit):
            load_config('/path/to/missing/config.yaml')
    
    def test_load_no_config(self):
        """Test when no config file is provided"""
        config = load_config(None)
        assert config == {}
    
    @pytest.mark.skipif('yaml' not in sys.modules, reason="PyYAML not installed")
    def test_load_invalid_yaml(self, temp_dir):
        """Test loading invalid YAML"""
        bad_config = temp_dir / "bad.yaml"
        bad_config.write_text("invalid: yaml: content:")
        
        with pytest.raises(SystemExit):
            load_config(str(bad_config))

class TestApplyConfigToArgs:
    """Test applying configuration to arguments"""
    
    def test_apply_global_config(self):
        """Test applying global configuration"""
        # Create mock args object
        class Args:
            command = 'nt'
            data_dir = None
            workers = None
        
        args = Args()
        config = {
            'global': {
                'data_dir': '/config/data',
                'workers': 16
            }
        }
        
        apply_config_to_args(args, config)
        assert args.data_dir == '/config/data'
        assert args.workers == 16
    
    def test_apply_command_config(self):
        """Test applying command-specific configuration"""
        class Args:
            command = 'pm'
            total_cutoff = None
            per_file_cutoff = None
        
        args = Args()
        config = {
            'pm': {
                'total_cutoff': 5,
                'per_file_cutoff': 2
            }
        }
        
        apply_config_to_args(args, config)
        assert args.total_cutoff == 5
        assert args.per_file_cutoff == 2
    
    def test_cli_overrides_config(self):
        """Test that CLI arguments override config"""
        class Args:
            command = 'nt'
            workers = 8  # Set via CLI
        
        args = Args()
        config = {
            'global': {
                'workers': 16  # In config
            }
        }
        
        apply_config_to_args(args, config)
        assert args.workers == 8  # CLI value preserved