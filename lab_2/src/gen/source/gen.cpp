#include <iostream>
#include <random>
#include <bitset>


class PRNG64 {
private:
    std::mt19937_64 engine;

public:
    PRNG64() {
        std::random_device device;
        engine.seed( device() );
    }

    uint64_t random64() {
        return engine();
    }
};


void print128(PRNG64& generator) {
    uint64_t part1 = generator.random64();
    uint64_t part2 = generator.random64();

    std::bitset<64> bin1(part1);
    std::bitset<64> bin2(part2);

    std::cout << bin1 << bin2;
}


int main() {
    PRNG64 generator;

    print128(generator);

    return 0;
}