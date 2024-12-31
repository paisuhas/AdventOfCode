#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>

int main() {
    std::ifstream input("input.txt");
    long n1, n2, sum;
    std::vector<long> list1, list2;
    std::unordered_map<long, unsigned> map1, map2;

    for (std::string line; std::getline(input, line);) {
        std::stringstream ss(line);
        ss >> n1 >> n2;
        list1.push_back(n1);
        list2.push_back(n2);
    }

    std::sort(list1.begin(), list1.end());
    std::sort(list2.begin(), list2.end());

    sum = 0;
    for (auto i = 0; i < list1.size(); i++) {
        n1 = list1[i];
        n2 = list2[i];
        sum += std::abs(n1 - n2);
        // std::cout << n1 << " " << n2 << "\n";
    }
    std::cout << sum << std::endl;

    for (const auto& elem: list1)
        if (map1.contains(elem))
            map1[elem] += 1;
        else
            map1[elem] = 1;

    for (const auto& elem: list2)
        if (map2.contains(elem))
            map2[elem] += 1;
        else
            map2[elem] = 1;

    sum = 0;
    for (const auto& [key, _] : map1) {
        // std::cout << key << " " << value << " " << map2[key] << "\n";
        sum += key * map2[key];
    }
    std::cout << sum << std::endl;
}