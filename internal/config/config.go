package config

import (
	"os"
	"strconv"
)

type Config struct {
	Server  ServerConfig
	Engine  EngineConfig
	Logging LoggingConfig
}

type ServerConfig struct {
	Port         string
	ReadTimeout  int
	WriteTimeout int
}

type EngineConfig struct {
	ModelPath     string
	NThreads      int
	NGPULayers    int
	ContextLength int
}

type LoggingConfig struct {
	Level string
}

func Load() *Config {
	return &Config{
		Server: ServerConfig{
			Port:         getEnv("APP_SERVER_PORT", ":8080"),
			ReadTimeout:  getEnvInt("APP_SERVER_READ_TIMEOUT", 30),
			WriteTimeout: getEnvInt("APP_SERVER_WRITE_TIMEOUT", 30),
		},
		Engine: EngineConfig{
			ModelPath:     getEnv("APP_ENGINE_MODEL_PATH", "./model.gguf"),
			NThreads:      getEnvInt("APP_ENGINE_N_THREADS", 4),
			NGPULayers:    getEnvInt("APP_ENGINE_N_GPU_LAYERS", 32),
			ContextLength: getEnvInt("APP_ENGINE_CONTEXT_LENGTH", 2048),
		},
		Logging: LoggingConfig{
			Level: getEnv("APP_LOGGING_LEVEL", "info"),
		},
	}
}

func getEnv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func getEnvInt(key string, def int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return def
}
