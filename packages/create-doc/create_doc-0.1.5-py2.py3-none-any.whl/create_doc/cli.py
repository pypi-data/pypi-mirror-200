import click
import json
import os
from dotenv import load_dotenv
import create_doc.analyze_with_gpt as gpt
import create_doc.analyze_module_dependencies as analyze_module_dependencies
from create_doc import __version__


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
def init():
    """Initialize the application"""
    click.echo('Initializing the application...')

    if os.path.isfile('./.create_doc.json'):
        confirm_overwrite = input('.create_doc.json already exists. Do you want to overwrite it? (y/n): ')
        if confirm_overwrite.lower() != 'y':
            exit()

    json_data = {
        "project_root_path": "",
        "output_path": "docs",
        "gpt_processors": [
            {
                "name": "forms",
                "input_paths": ["src"],
                "output_sub_path": "forms",
                "file_extensions": [".html"],
                "from_dir": "",
                "to_dir": "",
                "from_file": "",
                "to_file": "",
                "gpt_model_id": "gpt-3.5-turbo",
                "gpt_model_token_limit": 4096,
                "gpt_prompts": [
                    {
                        "role": "system",
                        "content": "You are a technical writer of user manuals. " +
                                   "You are working on a project to create application documentation from HTML code. " +
                                   "The result is in markdown format. " +
                                   "The first part of the documentation should contain a concise " +
                                   "description of the page from a user perspective. " +
                                   "The second part should contain instructions for using the page.",
                        "content_file_path": ""
                    }
                ],
                "angular_skip_html_router_outlet": True,
                "angular_router_outlet_message": "This page contains angular router-outlet tag. " +
                                                 "This means that this page contains subcomponents.",
                "content_title": "Content",
                "add_dependency_links": True,
                "dependency_link_text": "Dependency",
                "add_file_path": True
            }
        ],
        "applipress_processors": [
            {
                "name": "forms",
                "input_paths": ["src"],
                "output_sub_path": "forms",
                "file_extensions": [".html"],
                "from_form": "",
                "to_form": "",
                "gpt_model_id": "gpt-3.5-turbo",
                "gpt_model_token_limit": 4096,
                "gpt_prompts": [
                    {
                        "role": "system",
                        "content": "You are a technical writer of user manuals. " +
                                   "You are working on a project to create application documentation from HTML code. " +
                                   "The result is in markdown format. " +
                                   "The first part of the documentation should contain a concise " +
                                   "description of the page from a user perspective. " +
                                   "The second part should contain instructions for using the page.",
                        "content_file_path": ""
                    }
                ],
                "angular_skip_html_router_outlet": True,
                "angular_router_outlet_message": "This page contains angular router-outlet tag. " +
                                                 "This means that this page contains subcomponents.",
                "content_title": "Content",
                "add_dependency_links": True,
                "dependency_link_text": "Dependency",
                "add_file_path": True
            }
        ],
        "dependency_processors": [
            {
                "name": "typescript",
                "input_paths": ["src"],
                "output_sub_path": "dependencies",
                "summary_depth": 1,
                "include_only": "^src",
            }
        ]
    }

    with open('./.create_doc.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    click.echo("Created file .create_doc.json.")
    click.echo("This file will be used to configure the project documentation generation.")
    click.echo("Edit the file to your liking.")

    check_openapi_key()
    analyze_module_dependencies.init_dependecy_cruiser('.')

    return 0


@cli.command()
@click.argument('processor_name', type=str, default='all')
def gpt_process(processor_name):
    """Process files with GPT and create markdown files."""
    click.echo('GPT processing files...')
    click.echo('Using ' + str(processor_name) + ' processor(s)')

    check_openapi_key()
    config = get_config()
    gpt.init_env()

    if processor_name == 'all':
        for processor in config['gpt_processors']:
            gpt_process_processor(processor, config)
    else:
        processor = None

        # find processor by name in config['gpt_processors']
        for p in config['gpt_processors']:
            if p['name'] == processor_name:
                processor = p
                break

        if processor is not None:
            gpt_process_processor(processor, config)
        else:
            click.echo('Processor ' + processor_name + ' not found.')
            return 1

    click.echo('Done GPT processing')
    return 0


def gpt_process_processor(processor, config):
    click.echo('Processing processor ' + processor['name'])
    # for all paths in processor input paths
    output_path = config['output_path'] + '/' + processor['output_sub_path']
    from_dir = processor.get('from_dir')
    to_dir = processor.get('to_dir')
    from_file = processor.get('from_file')
    to_file = processor.get('to_file')
    for path in processor['input_paths']:
        click.echo('Processing path ' + path)
        # analyze html files
        gpt.analyze_files(config['project_root_path'], path, output_path, from_dir, to_dir, from_file, to_file,
                          processor['gpt_model_id'], processor['gpt_model_token_limit'], processor['gpt_prompts'],
                          processor['angular_skip_html_router_outlet'], processor['angular_router_outlet_message'],
                          processor['content_title'], processor['file_extensions'],
                          processor['add_dependency_links'], processor['add_file_path'],
                          processor['dependency_link_text'])


@cli.command()
@click.argument('processor_name', type=str, default='all')
def applipress_process(processor_name):
    """Process applipress forms with GPT and create markdown files."""
    click.echo('GPT processing applipress forms...')
    click.echo('Using ' + str(processor_name) + ' processor(s)')

    check_openapi_key()
    config = get_config()
    gpt.init_env()

    if processor_name == 'all':
        for processor in config['applipress_processors']:
            applipress_process_processor(processor, config)
    else:
        processor = None

        # find processor by name in config['gpt_processors']
        for p in config['applipress_processors']:
            if p['name'] == processor_name:
                processor = p
                break

        if processor is not None:
            applipress_process_processor(processor, config)
        else:
            click.echo('Processor ' + processor_name + ' not found.')
            return 1

    click.echo('Done GPT processing applipress forms')
    return 0


def applipress_process_processor(processor, config):
    click.echo('Processing processor ' + processor['name'])
    # for all paths in processor input paths
    output_path = config['output_path'] + '/' + processor['output_sub_path']
    from_form = processor.get('from_form')
    to_form = processor.get('to_form')
    for path in processor['input_paths']:
        click.echo('Processing path ' + path)
        # analyze html files
        gpt.analyze_applipress_forms(config['project_root_path'], path, output_path, from_form, to_form,
                          processor['gpt_model_id'], processor['gpt_model_token_limit'], processor['gpt_prompts'],
                          processor['angular_skip_html_router_outlet'], processor['angular_router_outlet_message'],
                          processor['content_title'], processor['file_extensions'],
                          processor['add_dependency_links'], processor['add_file_path'],
                          processor['dependency_link_text'])

@cli.command()
@click.argument('processor_name', type=str, default='all')
def analyze_dependencies(processor_name):
    """Analyze dependencies and create documentation."""

    click.echo('Processing application dependencies...')
    click.echo('Using ' + str(processor_name) + ' processor(s)')

    config = get_config()
    project_directory_path = config['project_root_path']

    if processor_name == 'all':
        for processor in config['dependency_processors']:
            process_dependencies_processor(processor, config)
    else:
        processor = None
        for p in config['dependency_processors']:
            if p['name'] == processor_name:
                processor = p
                break

        if processor is not None:
            process_dependencies_processor(processor, config)
        else:
            click.echo('Processor ' + processor_name + ' not found.')
            return 1

    return 0


def process_dependencies_processor(processor, config):
    click.echo('Processing processor ' + processor['name'])
    # for all paths in processor input paths
    output_path = config['output_path'] + '/' + processor['output_sub_path']
    for path in processor['input_paths']:
        click.echo('Processing path ' + path)
        # analyze html files
        analyze_module_dependencies.process_directory_dependencies(config['project_root_path'], path, output_path,
                                                                   processor['summary_depth'],
                                                                   processor['include_only'])


def read_config_file():
    with open('./.create_doc.json', 'r') as file:
        return json.load(file)


def get_config():
    config = read_config_file()

    # get current working directory
    cwd = os.getcwd()
    # get project root path
    config['project_root_path'] = create_abs_path(cwd, config['project_root_path'])
    config['output_path'] = create_abs_path(cwd, config['output_path'])

    # for each processor in gpt processors, create absolute input paths
    for processor in config['gpt_processors']:
        processor['input_paths'] = create_abs_paths(cwd, processor['input_paths'])

    # for each processor in dependency processors, create absolute input paths
    for processor in config['dependency_processors']:
        processor['input_paths'] = create_abs_paths(cwd, processor['input_paths'])

    # print config
    # print('Using configuration:')
    # print(json.dumps(config, indent=4))

    return config


def create_abs_path(cwd, path):
    # if p
    if not os.path.isabs(path):
        return os.path.join(cwd, path)
    return path


def create_abs_paths(cwd, paths):
    for i, path in enumerate(paths):
        if not os.path.isabs(path):
            paths[i] = os.path.join(cwd, path)
    return paths


def check_openapi_key():
    # read environment variable OPENAI_API_KEY

    load_dotenv()
    openapi_key = os.getenv('OPENAI_API_KEY')
    if not openapi_key:
        click.echo('OPENAI_API_KEY environment variable not set.')
        click.echo('Please set it to your OpenAPI key.')
        return False
    return True


if __name__ == '__main__':
    cli()
