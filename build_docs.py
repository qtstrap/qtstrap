from lazydocs import generate_docs

# The parameters of this function correspond to the CLI options
generate_docs(
    ["qtstrap"],
    output_path="./docs/api",
    overview_file='overview.md',
    src_base_url='https://github.com/qtstrap/qtstrap/blob/master',
    ignored_modules = [
        'qt',
        'version',
    ]
)
