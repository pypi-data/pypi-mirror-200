import json
import re

import openai
from dotenv import load_dotenv
import os
import tiktoken

from create_doc.utils import check_output_path


def init_env():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai.api_key


def get_template_directories(template_name):
    template_defs = [
        {'name': 'default', 'dirs': ['list', 'detail', 'update', 'delete']},
        {'name': 'form', 'dirs': ['update']},
        {'name': 'form-routable', 'dirs': ['update']},
        {'name': 'form-with-status', 'dirs': ['update']},
        {'name': 'layout-accordion', 'dirs': ['layout']},
        {'name': 'layout-column', 'dirs': []},
        {'name': 'layout-hsplitter', 'dirs': []},
        {'name': 'layout-panel', 'dirs': []},
        {'name': 'layout-rows2', 'dirs': []},
        {'name': 'layout-tabs', 'dirs': []},
        {'name': 'layout-top-tabs', 'dirs': []},
        {'name': 'png-table', 'dirs': ['list', 'detail', 'update', 'delete']},
        {'name': 'png-table-c', 'dirs': ['list']},
        {'name': 'table', 'dirs': ['list']},
        {'name': 'wizard-form', 'dirs': ['update']}
    ]
    # find the template by name
    template_def = next((x for x in template_defs if x['name'] == template_name), None)
    if template_def:
        return template_def['dirs']
    else:
        return []


def load_text(filepath):
    """
    Load text from the given file path.

    Args:
        filepath (str): The file path of the text.

    Returns:
        str: The content of the text.
    """
    with open(filepath, "r") as f:
        text = f.read()
    return text


def chat_gpt_conversation(conversation, model_id):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    print('Token consumed: {0}'.format(api_usage['total_tokens']))
    token_consumed = api_usage['total_tokens']
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return {'conversation': conversation, 'tokens_consumed': token_consumed}


def init_gpt_with_config_prompts(gpt_prompts):
    _conversation = []
    for gpt_prompt in gpt_prompts:
        content_file_path = gpt_prompt.get('content_file_path')
        prompt_content = ""
        if content_file_path:
            prompt_content = load_text(content_file_path)
        else:
            prompt_content = gpt_prompt.get('content')

        role = gpt_prompt.get('role', 'system')
        if prompt_content and len(prompt_content) > 0:
            _conversation.append({'role': role, 'content': prompt_content})

    return _conversation


def num_tokens_from_messages(messages, model):
    """
    Returns the number of tokens used by a list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo" or model == "gpt-4":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def traverse_directory(directory_path):
    directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    return directories


def get_all_files_in_directory_and_subdirectories(directory, file_extensions):
    # get all files in directory and its subdirectories with the given file_filter
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check if python string ends with a string defined in array file_extensions
            if file.endswith(tuple(file_extensions)):
                file_list.append(os.path.join(root, file))
    return file_list


def open_content_markdown(output_path, content_title):
    # create path from root_path and directory_path
    check_output_path(output_path)
    output_file = os.path.join(output_path, 'content.md')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    output_file.write('# ' + content_title + '\n')
    return output_file


def add_content_markdown(output_file, directory_path, content_title):
    # write markdown text
    output_file.write('[[' + directory_path + '|' + content_title + ']]\n\n')


def close_content_markdown(output_file):
    output_file.close()


def add_dependency_markdown(output_file, directory_path):
    # write markdown text
    output_file.write('[[' + directory_path + '-module-dependency|' + directory_path + ']]\n\n')


def open_component_markdown(output_path, directory_path):
    # create path from root_path and directory_path
    check_output_path(output_path)
    output_file = os.path.join(output_path, directory_path + '.md')
    print('Creating markdown file: ' + output_file + '...')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    return output_file


def add_to_component_markdown(output_file, text):
    output_file.write(text + '\n\n')


def close_component_markdown(output_file):
    # close output file
    print('Closing markdown file...')
    output_file.close()


def create_title_for_file(file_path):
    # get file name
    file_name = os.path.basename(file_path)
    # remove extension
    file_name = os.path.splitext(file_name)[0]
    # replace _ with space
    file_name = file_name.replace('_', ' ')
    file_name = file_name.replace('.', ' ')

    # if file_name.endswith('.component'):
    #     file_name = file_name[:-len('.component')]
    # if file_name.endswith('.model'):
    #     file_name = file_name[:-len('.model')]
    # if file_name.endswith('.service'):
    #     file_name = file_name[:-len('.service')]

    # capitalize
    file_name = file_name.capitalize()
    return file_name


def create_filename_for_title(title):
    # replace space with _
    file_name = title.replace(' ', '_')
    # lowercase
    file_name = file_name.lower()
    return file_name


def filter_list(file_list, from_file, to_file):
    # filter files by from_file and to_file
    if from_file is not None and len(from_file) > 0:
        if from_file in file_list:
            from_file_index = file_list.index(from_file)
            file_list = file_list[from_file_index:]
        else:
            next_file_index = find_index_of_first_next_to_filename(file_list, from_file)
            file_list = file_list[next_file_index:]
    if to_file is not None and len(to_file) > 0:
        if to_file in file_list:
            to_file_index = file_list.index(to_file)
            file_list = file_list[:to_file_index + 1]
        else:
            next_file_index = find_index_of_last_before_filename(file_list, to_file)
            file_list = file_list[:next_file_index]
    return file_list


def filter_dict_with_name(file_list, from_file, to_file):
    # filter files by from_file and to_file
    if from_file is not None and len(from_file) > 0:
        next_file_index = find_index_of_first_next_to_filename_object(file_list, from_file)
        file_list = file_list[next_file_index:]
    if to_file is not None and len(to_file) > 0:
        next_file_index = find_index_of_last_before_filename_object(file_list, to_file)
        file_list = file_list[:next_file_index]
    return file_list


def filter_file_paths_with_filename(filepath_list, from_filename, to_filename):
    # filter files by from_file and to_file
    if from_filename is not None and len(from_filename) > 0:
        next_file_index = find_index_of_first_next_to_filename_without_path(filepath_list, from_filename)
        filepath_list = filepath_list[next_file_index:]
    if to_filename is not None and len(to_filename) > 0:
        next_file_index = find_index_of_last_before_filename_without_path(filepath_list, to_filename)
        filepath_list = filepath_list[:next_file_index]
    return filepath_list


def filter_out_filepaths_with_bck(filepath_list):
    # filter out files that contain bck
    return [file for file in filepath_list if 'bck' not in file.lower()]



def find_index_of_first_next_to_filename(file_list, from_file):
    for i, file in enumerate(file_list):
        if file >= from_file:
            return i

    return len(file_list)


def find_index_of_first_next_to_filename_without_path(filepath_list, from_file):
    # filepath_list is a list of file paths, extract file name from each path in a separate list without extension
    file_list = [os.path.splitext(os.path.basename(file))[0] for file in filepath_list]
    for i, file in enumerate(file_list):
        if file >= from_file:
            return i

    return len(file_list)



def find_index_of_first_next_to_filename_object(file_list, from_file):
    # file_list is a list of objects with name property, extract name property in a separate list
    file_list_names = [file.get('name') for file in file_list]
    for i, file in enumerate(file_list_names):
        if file >= from_file:
            return i

    return len(file_list)


def find_index_of_last_before_filename(file_list, from_file):
    for i, file in enumerate(file_list):
        if file >= from_file:
            return i

    return len(file_list)


def find_index_of_last_before_filename_without_path(filepath_list, from_file):
    # filepath_list is a list of file paths, extract file name from each path in a separate list without extension
    file_list = [os.path.splitext(os.path.basename(file))[0] for file in filepath_list]
    for i, file in enumerate(file_list):
        if file >= from_file:
            return i

    return len(file_list)


def find_index_of_last_before_filename_object(file_list, from_file):
    # file_list is a list of objects with name property, extract name property in a separate list
    file_list_names = [file.get('name') for file in file_list]
    for i, file in enumerate(file_list_names):
        if file >= from_file:
            return i

    return len(file_list)


def analyze_files(_project_root_directory, _input_directory, _output_directory, from_dir, to_dir, from_file, to_file,
                  _model_id, _model_token_limit,
                  _gpt_prompts, _skip_router_outlet, _skip_router_outlet_text, _content_title, _file_extensions,
                  _add_dependency_link, _add_file_path, _dependency_link_text
                  ):
    directories = traverse_directory(_input_directory)
    # if length of directories is 0, add _input_directory to directories
    process_directories = True
    if len(directories) == 0:
        directories.append(_input_directory)
        process_directories = False

    # sort directories
    directories.sort()
    directories = filter_list(directories, from_dir, to_dir)

    content_file = open_content_markdown(_output_directory, _content_title)

    if _add_dependency_link and _dependency_link_text is not None and len(_dependency_link_text) > 0:
        _dependency_link_text = _dependency_link_text + ':'

    total_tokens = 0

    for directory in directories:
        print('Processing directory: {0} ----------------------'.format(directory))
        file_list = get_all_files_in_directory_and_subdirectories(
            os.path.join(_input_directory, directory),
            _file_extensions)
        # if file list is not empty, process files
        if file_list:
            print('Processing files: ')
            file_list.sort()
            if (from_file is not None and len(from_file) > 0) or (to_file is not None and len(to_file) > 0):
                file_list = filter_list(file_list, from_file, to_file)

            description_file = None
            if process_directories:
                description_file = open_component_markdown(_output_directory, directory)
                add_dependency_markdown(content_file, directory)
                add_to_component_markdown(description_file, '# ' + directory + '\n\n')
                if _add_dependency_link:
                    add_to_component_markdown(description_file,
                                              _dependency_link_text + '[[' + directory + '-module-dependency|' +
                                              directory + ']]\n\n')

            for file in file_list:
                # create relative file path from project root directory and file
                print(file)
                title = create_title_for_file(file)
                print(title)
                file_relative_path = os.path.relpath(file, _project_root_directory)
                if not process_directories:
                    file_name = create_filename_for_title(title)
                    description_file = open_component_markdown(_output_directory, file_name)
                    add_dependency_markdown(content_file, file_name)
                    add_to_component_markdown(description_file, '# ' + title + '\n')
                    if _add_file_path:
                        add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')

                    if _add_dependency_link:
                        add_to_component_markdown(description_file,
                                                  _dependency_link_text + '[[' + directory + '-module-dependency|'
                                                  + directory + ']]\n\n')

                file_text = load_text(file)
                # if file_text contains string <router-outlet> show message that this component contains router-outlet
                if '<router-outlet>' in file_text:
                    add_to_component_markdown(description_file, '# ' + title + '\n\n')

                    add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')
                    add_to_component_markdown(description_file, _skip_router_outlet_text)
                else:
                    conversation = init_gpt_with_config_prompts(_gpt_prompts)
                    conversation.append({'role': 'user', 'content': file_text})
                    num_tokens = num_tokens_from_messages(conversation, _model_id)
                    if num_tokens <= _model_token_limit:
                        result = chat_gpt_conversation(conversation, _model_id)
                        print('----------------------')
                        print('{0}\n'.format(result['conversation'][-1]['content'].strip()))

                        if process_directories:
                            add_to_component_markdown(description_file, '## ' + title + '\n\n')
                            if _add_file_path:
                                add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')

                        add_to_component_markdown(description_file, result['conversation'][-1]['content'].strip())
                        total_tokens += result['tokens_consumed']
                    else:
                        add_to_component_markdown(description_file,
                                                  '## Error processing file: {0} - too many tokens consumed: {1}'
                                                  .format(file, num_tokens))

            close_component_markdown(description_file)
    close_content_markdown(content_file)
    print('Total tokens consumed: {0}'.format(total_tokens))
    return 0


def extract_name_properties(json_data):
    result = {}

    if 'name' in json_data:
        result['name'] = json_data['name']

    if 'subforms' in json_data:
        result['subforms'] = []
        for subform in json_data['subforms']:
            extracted_subform = extract_name_properties(subform)
            result['subforms'].append(extracted_subform)

    return result


def extract_names(data):
    names = []

    if 'name' in data:
        names.append({"name": data['name'], "template": data['body']['template']})

    if 'subforms' in data['body']:
        for subform in data['body']['subforms']:
            names.extend(extract_names(subform))

    return names


def extract_forms_from_json_file(json_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        names = extract_names(data)
        return names


def kebabCase(string):
    # Insert a space before capital letters if it's not the beginning or followed by a lowercase letter
    string = re.sub(r'(?<=[a-z])([A-Z])|(?<=[A-Z])([A-Z](?=[a-z]))', r' \1\2', string)

    # Replace non-word characters with spaces
    string = re.sub(r'\W+', ' ', string)

    # Replace multiple spaces with a single space
    string = re.sub(r'\s+', ' ', string).strip()

    # Replace spaces with hyphens and convert to lowercase
    string = string.replace(' ', '-').lower()

    return string


def analyze_applipress_forms(_project_root_directory, _input_directory, _output_directory, from_form, to_form,
                             _model_id, _model_token_limit,
                             _gpt_prompts, _skip_router_outlet, _skip_router_outlet_text, _content_title,
                             _file_extensions,
                             _add_dependency_link, _add_file_path, _dependency_link_text
                             ):
    content_file = open_content_markdown(_output_directory, _content_title)

    if _add_dependency_link and _dependency_link_text is not None and len(_dependency_link_text) > 0:
        _dependency_link_text = _dependency_link_text + ':'

    total_tokens = 0

    # get all json form definition files
    json_files = get_all_files_in_directory_and_subdirectories(
        os.path.join(_project_root_directory, '.jhipster/forms'),
        ['.json'])
    json_files.sort()
    json_files = filter_file_paths_with_filename(json_files, from_form, to_form)
    # json_files = filter_out_filepaths_with_bck(json_files)

    for json_file in json_files:
        form_names = extract_forms_from_json_file(json_file)
        # form_names = filter_dict_with_name(form_names, from_form, to_form)
        description_file = None

        root_form = ''
        for index, form_name in enumerate(form_names):
            dir_names = [kebabCase(form_name['name'])]
            if index == 0:
                print('Processing form: {0} ----------------------'.format(form_name['name']))
                description_file = open_component_markdown(_output_directory, root_form)
                root_form = kebabCase(form_name['name'])
                dir_names = get_template_directories(form_name['template'])
                if len(dir_names) > 0:
                    add_content_markdown(content_file, root_form, form_name['name'])
                    add_to_component_markdown(description_file, '# ' + form_name['name'] + '\n\n')
                    for dir_name in dir_names:
                        form_path = os.path.join(_project_root_directory, 'src/main/webapp/app/forms', root_form, dir_name)
                        process_form_directory(form_path, description_file, _model_id, _model_token_limit, _gpt_prompts,
                                               _skip_router_outlet, _skip_router_outlet_text)
            else:
                subform_dirs = get_template_directories(form_name['template'])
                if len(subform_dirs) > 0:
                    dir_name = kebabCase(form_name['name'])
                    print('Processing subform: {0} ----------------------'.format(form_name['name']))
                    add_to_component_markdown(description_file, '## ' + form_name['name'] + '\n\n')
                    form_path = os.path.join(_project_root_directory, 'src/main/webapp/app/forms', root_form, dir_name)
                    process_form_directory(form_path, description_file, _model_id, _model_token_limit, _gpt_prompts,
                                           _skip_router_outlet, _skip_router_outlet_text)

        if description_file is not None:
            close_component_markdown(description_file)

    close_content_markdown(content_file)
    print('Total tokens consumed: {0}'.format(total_tokens))
    return 0


def process_form_directory(_form_dir_path, _description_file, _model_id, _model_token_limit, _gpt_prompts,
                           _skip_router_outlet, _skip_router_outlet_text):
    """
    Process a single form directory
    """
    print('Processing form directory: {0} ----------------------'.format(_form_dir_path))
    _file_extensions = ['.html']
    directories = traverse_directory(_form_dir_path)
    if directories is None or len(directories) == 0:
        directories = [ _form_dir_path]
    directories.sort()
    for directory in directories:
        file_list = get_all_files_in_directory_and_subdirectories(
            os.path.join(_form_dir_path, directory),
            _file_extensions)
        # if file list is not empty, process files
        if file_list:
            file_list.sort()
            for file in file_list:
                process_form_file(file, _description_file, _model_id, _model_token_limit, _gpt_prompts,
                                  _skip_router_outlet, _skip_router_outlet_text)
    return 0


def process_form_file(_form_file_path, _description_file, _model_id, _model_token_limit, _gpt_prompts,
                      _skip_router_outlet, _skip_router_outlet_text):
    """
    Process a single form file
    :param _form_file_path: form file to process
    :param _description_file: file to write description to
    :param _model_id: GPT model id
    :param _model_token_limit: GPT model token limit
    :param _gpt_prompts: GPT prompts
    :param _skip_router_outlet: skip router outlet
    :param _skip_router_outlet_text: skip router outlet text
    :return: 0
    """
    print('Processing form file: {0} ----------------------'.format(_form_file_path))

    conversation = init_gpt_with_config_prompts(_gpt_prompts)
    conversation.append({'role': 'user', 'content': load_text(_form_file_path)})
    num_tokens = num_tokens_from_messages(conversation, _model_id)
    if num_tokens <= _model_token_limit:
        result = chat_gpt_conversation(conversation, _model_id)
        print('----------------------')
        print('{0}\n'.format(result['conversation'][-1]['content'].strip()))

        add_to_component_markdown(_description_file, result['conversation'][-1]['content'].strip())
    else:
        add_to_component_markdown(_description_file,
                                  '## Error processing form file: {0} - too many tokens consumed: {1}'
                                  .format(_form_file_path, num_tokens))

    return 0
