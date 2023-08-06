## create_doc

Generate angular project documentation using GPT and dependency-cruiser.

- Free software: MIT license

### Features

- Create documentation for your project using GPT. Analyze html files or other file types and generate a markdown file with the documentation.

- Create module dependency documentation using dependency-cruiser static code analysis.

### Installation

- Install the package with pip:

        pip install create_doc

- Define the following environment variables:

        OPENAI_API_KEY: Your OpenAI API key

- Install the following tools used by the processors:
  - Install dependency-cruiser in the project you want to analyze


        npm install dependency-cruiser

  - or install dependency-cruiser globally to use it in other projects (it will show some warnings during processing

        npm install -g dependency-cruiser



### Usage

- Initialize a project with the following command:

        create_doc init

- Check the configuration file `.create_doc.json` created in the root of your project and adjust it to your needs. You can define multiple processors for gpt and dependencies.

- Create documentation for your project the following command:

        create_doc gpt-process

- You can also run the specific gpt processors with the following commands:

        create_doc gpt-process processor_name

- for example

        create_doc gpt-process forms

- Create documentation for your project dependencies with the following command:

        create_doc analyze-dependencies

- To run the specific dependency processors use the following commands:

        create_doc analyze-dependencies processor_name

### Credits

OpenAI API is used to generate the documentation.

- OpenAI API: https://openai.com/

Dependency-cruiser is used to analyze the dependencies of the project.

- Dependency-cruiser: https://github.com/sverweij/dependency-cruiser

Example angular form from https://github.com/gothinkster/angular-realworld-example-app

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

- Cookiecutter: https://github.com/audreyr/cookiecutter
- `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

