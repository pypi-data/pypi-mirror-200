import os


original_file_name = '__init__.py'

directory_name = 'functions'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

functions_found = []
current_function = None
with open(original_file_name, "r") as original_file:
    current_function = None
    current_function_lines = []
    for line in original_file:
        if line.startswith("def "):
            # If there was a previous function, save it to a file
            if current_function is not None:
                function_filename = os.path.join(directory_name, current_function + ".py")
                with open(function_filename, "w") as function_file:
                    function_file.write("".join(current_function_lines))
                    functions_found.append(function_filename)
                current_function = None
                current_function_lines = []
            
            # Get the function name
            function_name = line.split()[1].split("(")[0]
            current_function_lines.append(line)
            current_function = function_name
        elif line.startswith("import"):
            pass
        else:
            current_function_lines.append(line)

    # Save the last function to a file
    function_filename = os.path.join(directory_name, current_function + ".py")
    with open(function_filename, "w") as function_file:
        function_file.write("".join(current_function_lines))
        functions_found.append(function_filename)

print(len(functions_found))

check_words = ['math.', 'np.', 'pd.', 'plt.', 'os.', 'warnings.', 'sys.', 'copy.']
libraries = {'math.' : 'import math\n', 'np.' : 'import numpy as np\n', 'pd.' : 'import pandas as pd\n', 'plt.' : 'import matplotlib.pyplot as plt\n', 'os.' : 'import os\n', 'warnings.' : 'import warnings\n', 'sys.' : 'import sys\n', 'copy.' : 'import copy\n'}
for func_name in functions_found:
    check_words.append((func_name.split('/')[1]).split('.')[0] + '(')
# loop over the functions files to determine and import the dependencies
for filename in os.listdir(directory_name):
    imports = []
    if not filename.endswith('.py'):
        continue
    file_path = os.path.join(directory_name, filename)
    with open(file_path, 'r') as f:
        file_contents = f.read() # file_contents is a string containing the contents of the file
        for word in check_words:
            if word in file_contents and word[:-1] not in filename:
                if '.' in word:
                    imports.append(libraries[word])
                elif '(' in word:
                    imports.append('import ' + word[:-1] + '\n')
        if len(imports) > 0:
            imports.append('\n\n')
    with open(file_path, 'w') as f:
        f.writelines(imports)
        f.write(file_contents)
