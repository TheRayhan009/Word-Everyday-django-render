import subprocess
import os
cpp_code = """
#include <iostream>
using namespace std;

int main() {
    int n;
    cin>>n;
    cout << n;
    return 0;
}
"""

with open("generated.cpp", "w") as f:
    f.write(cpp_code)

subprocess.run(['g++', 'generated.cpp', '-o', 'generated'])
subprocess.run(['./generated'])  # Or ['generated.exe'] on Windows
