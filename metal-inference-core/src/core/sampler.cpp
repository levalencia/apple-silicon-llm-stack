#include "metal_inference/types.h"
#include <vector>
#include <random>

namespace metal_inference {

class Sampler {
public:
    virtual ~Sampler() = default;
    virtual int sample(const std::vector<float>& logits) = 0;
};

class GreedySampler : public Sampler {
public:
    int sample(const std::vector<float>& logits) override {
        int max_idx = 0;
        float max_val = logits[0];
        
        for (size_t i = 1; i < logits.size(); ++i) {
            if (logits[i] > max_val) {
                max_val = logits[i];
                max_idx = static_cast<int>(i);
            }
        }
        
        return max_idx;
    }
};

class TopKSampler : public Sampler {
public:
    explicit TopKSampler(int k) : k_(k) {}
    
    int sample(const std::vector<float>& logits) override {
        return 0;
    }
    
private:
    int k_;
};

}
