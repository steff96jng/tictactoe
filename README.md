# Setup

# Requirements
- Python 3.7 __x64__
- venv
- (Windows only) [Enable windows long path](https://superuser.com/questions/1119883/windows-10-enable-ntfs-long-paths-policy-option-missing)

# Setup

## Windows
1. ```
    pip install -U pip virtualenv
    ```
2. ```
    virtualenv --system-site-packages -p python ./venv
    ```
3. ```
    .\venv\Scripts\activate
    ```

4. ```
    deactivate  # don't exit until you're done using TensorFlow
    ```

## OSX/Ubuntu
1. ```
    virtualenv --system-site-packages -p python3 ./venv
    ```
2. ```
    source ./venv/bin/activate  # sh, bash, ksh, or zsh
    ```
3. ```
    pip install --upgrade pip
    pip list  # show packages installed within the virtual environment
    ```

4. ```
    deactivate  # don't exit until you're done using TensorFlow
    ```

https://www.tensorflow.org/install/pip

