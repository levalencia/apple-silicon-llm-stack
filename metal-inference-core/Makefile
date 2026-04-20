.PHONY: help build test clean lint format check bench

help:
	@echo "Metal Inference Core - Available targets:"
	@echo ""
	@echo "  build    Build the library and CLI"
	@echo "  test     Run tests"
	@echo "  bench    Run benchmarks"
	@echo "  lint     Run clang-tidy"
	@echo "  format   Format code with clang-format"
	@echo "  check    Run all checks"
	@echo "  clean    Clean build artifacts"

build:
	cmake -B build -DCMAKE_BUILD_TYPE=Release
	cmake --build build -j$$(sysctl -n hw.logicalcpu)

test: build
	cd build && ctest --output-on-failure

bench: build
	./build/bin/inference_cli bench ./model.gguf

lint:
	find include src tests -name '*.cpp' -o -name '*.h' -o -name '*.mm' | \
		xargs clang-tidy

format:
	find include src tests -name '*.cpp' -o -name '*.h' -o -name '*.mm' | \
		xargs clang-format -i

check: lint format test

clean:
	rm -rf build/
