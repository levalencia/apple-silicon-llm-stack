package config

import "testing"
import "os"

func TestLoadDefaults(t *testing.T) {
	os.Unsetenv("APP_SERVER_PORT")
	os.Unsetenv("APP_SERVER_READ_TIMEOUT")
	os.Unsetenv("APP_ENGINE_MODEL_PATH")

	cfg := Load()

	if cfg.Server.Port != ":8080" {
		t.Errorf("expected port :8080, got %s", cfg.Server.Port)
	}
	if cfg.Server.ReadTimeout != 30 {
		t.Errorf("expected read timeout 30, got %d", cfg.Server.ReadTimeout)
	}
	if cfg.Engine.ModelPath != "./model.gguf" {
		t.Errorf("expected model path ./model.gguf, got %s", cfg.Engine.ModelPath)
	}
	if cfg.Engine.NThreads != 4 {
		t.Errorf("expected n_threads 4, got %d", cfg.Engine.NThreads)
	}
	if cfg.Logging.Level != "info" {
		t.Errorf("expected level info, got %s", cfg.Logging.Level)
	}
}

func TestLoadEnvOverrides(t *testing.T) {
	os.Setenv("APP_SERVER_PORT", ":9090")
	os.Setenv("APP_SERVER_READ_TIMEOUT", "60")
	os.Setenv("APP_ENGINE_MODEL_PATH", "/custom/path/model.gguf")
	os.Setenv("APP_ENGINE_N_THREADS", "8")
	os.Setenv("APP_LOGGING_LEVEL", "debug")
	defer func() {
		os.Unsetenv("APP_SERVER_PORT")
		os.Unsetenv("APP_SERVER_READ_TIMEOUT")
		os.Unsetenv("APP_ENGINE_MODEL_PATH")
		os.Unsetenv("APP_ENGINE_N_THREADS")
		os.Unsetenv("APP_LOGGING_LEVEL")
	}()

	cfg := Load()

	if cfg.Server.Port != ":9090" {
		t.Errorf("expected port :9090, got %s", cfg.Server.Port)
	}
	if cfg.Server.ReadTimeout != 60 {
		t.Errorf("expected read timeout 60, got %d", cfg.Server.ReadTimeout)
	}
	if cfg.Engine.ModelPath != "/custom/path/model.gguf" {
		t.Errorf("expected model path /custom/path/model.gguf, got %s", cfg.Engine.ModelPath)
	}
	if cfg.Engine.NThreads != 8 {
		t.Errorf("expected n_threads 8, got %d", cfg.Engine.NThreads)
	}
	if cfg.Logging.Level != "debug" {
		t.Errorf("expected level debug, got %s", cfg.Logging.Level)
	}
}

func TestGetEnvDefault(t *testing.T) {
	os.Unsetenv("NONEXISTENT_KEY")

	result := getEnv("NONEXISTENT_KEY", "default_value")

	if result != "default_value" {
		t.Errorf("expected default_value, got %s", result)
	}
}

func TestGetEnvOverride(t *testing.T) {
	os.Setenv("TEST_KEY", "test_value")
	defer os.Unsetenv("TEST_KEY")

	result := getEnv("TEST_KEY", "default_value")

	if result != "test_value" {
		t.Errorf("expected test_value, got %s", result)
	}
}

func TestGetEnvInt(t *testing.T) {
	os.Setenv("INT_TEST", "42")
	defer os.Unsetenv("INT_TEST")

	result := getEnvInt("INT_TEST", 10)

	if result != 42 {
		t.Errorf("expected 42, got %d", result)
	}
}

func TestGetEnvIntDefault(t *testing.T) {
	os.Unsetenv("NONEXISTENT_INT")

	result := getEnvInt("NONEXISTENT_INT", 99)

	if result != 99 {
		t.Errorf("expected 99, got %d", result)
	}
}
