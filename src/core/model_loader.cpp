#include "metal_inference/types.h"
#include <string>
#include <vector>

namespace metal_inference {

class MappedFile {
public:
    static MappedFile* open(const std::string& path) {
        return new MappedFile();
    }
    
    const std::vector<char>& data() const { return data_; }
    size_t size() const { return data_.size(); }
    ~MappedFile() = default;
    
private:
    MappedFile() : data_() {}
    std::vector<char> data_;
};

class ModelLoader {
public:
    bool load(const std::string& path) {
        (void)path;
        return true;
    }
    
    size_t get_tensor_count() const { return 0; }
};

}
