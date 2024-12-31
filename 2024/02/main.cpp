#include <algorithm>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::ifstream input("test.txt");
    auto safe_count = 0u;

    for (std::string line;std::getline(input, line);) {
        long prev, curr, diff;
        bool decreasing, safe = false;
        std::stringstream ss(line);

        ss >> prev >> curr;
        decreasing = curr < prev;
        diff = decreasing ? prev - curr : curr - prev;
        safe = (diff > 0 && diff < 4);
        prev = curr;
        while (safe && !ss.eof()) {
            ss >> curr;
            diff = decreasing ? prev - curr : curr - prev;
            safe = (diff > 0 && diff < 4);
            prev = curr;
        }
        if (safe)
            safe_count++;
    }
    std::cout << safe_count << std::endl;

    input.clear();
    input.seekg(0, std::ios::beg);

    safe_count = 0;
 
    std::vector<size_t> lens;
    for (std::string line;std::getline(input, line);) {
        long prev, curr;
        std::stringstream ss(line);
        std::vector<long> diffs;
        ss >> prev;
        do {
            ss >> curr;
            diffs.push_back(curr - prev);
            prev = curr;
        } while (!ss.eof());
        auto negatives = std::count_if(diffs.begin(), diffs.end(), [](auto i) { return i < 0; });
        auto positives = std::count_if(diffs.begin(), diffs.end(), [](auto i) { return i > 0; });
        auto total = diffs.size();
        if (total == positives || total == negatives || (positives == (total - 1) && negatives == 0) || (negatives == (total - 1) && positives == 0)) {
            if (std::all_of(diffs.begin(), diffs.end(), [](auto i) { auto d = std::abs(i); return (d >= 0 && d < 4);})) {
                safe_count++;
            } else if (std::count_if(diffs.begin(), diffs.end(), [](auto i) { auto d = std::abs(i); return (d == 0 || d >= 4); }) == 1) {
                for (const auto& diff: diffs)
                    std::cout << diff << " ";
                std::cout << std::endl;
            }
        }
        lens.push_back(diffs.size());
    }
    // std::cout << lens.size() << " " << *std::max_element(lens.begin(), lens.end()) << " " << *std::min_element(lens.begin(), lens.end()) <<std::endl;
    std::cout << safe_count << std::endl;
}