
# Oridati

Oridati is a minimal Python back-end framework for creating fast APIs based on example data, taking a bottom-up approach to data model design. Unlike traditional frameworks, Oridati allows developers to define the data model by creating instances of the data, and the framework infers the model by analyzing these instances.

## Features

- **Bottom-up Data Model Design**: Create instance data to define the data model, and let Oridati infer the schema based on the provided examples.
- **Incremental Iterative Process**: Continuously add or edit data instances to refine and evolve the data model.
- **Command-Line Interface (CLI)**: Use the CLI tools provided by Oridati to analyze the data, view inferred models, and generate or edit the final schema.
- **Generative Model**: Oridati utilizes generative modeling techniques to predict and complete the missing parts of the data model.
- **Instance Data Library**: Leverage the library of pre-existing instance data provided by Oridati to bootstrap your projects or as a reference for completing your own data instances.

## Getting Started

### Installation

1. Clone the Oridati repository:

   ```shell
   git clone https://github.com/nnehdi/oridati.git
   ```

2. Change into the project directory:

   ```shell
   cd oridati
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Usage

1. Add your example data instances as JSON files to the "data" directory.

2. Run the CLI command to analyze the data and infer the data model:

   ```shell
   python oridati.py analyze
   ```

3. View the inferred data model and make adjustments if necessary.

4. Use the CLI commands to generate or edit data based on the inferred model.

5. Repeat the process by adding or editing data instances as needed, and re-run the analysis command to update the inferred data model.

For detailed usage instructions and available CLI commands, refer to the [Documentation](documentation.md).

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or would like to contribute to Oridati, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

