# Contributing to Django SSO Engine

Thank you for your interest in contributing to Django SSO Engine. We welcome contributions from the community and appreciate your help in making this project better. Please take a moment to review this document for guidelines on how to contribute.

## Code of Conduct

Before contributing, please read our [Code of Conduct](CODE_OF_CONDUCT.md). We expect all contributors to follow these guidelines.

## How to Contribute

Here's how you can contribute to the Django SSO Engine:

1. **Fork the Repository**: Click the "Fork" button on the top right of the project's GitHub page to create your copy of the repository.

2. **Clone the Repository**: Clone the repository to your local machine using `git`. Replace `[your-fork]` with your GitHub username.

    ```bash
       git clone https://github.com/[your-fork]/Django-SSO-Engine.git
    ```

3. **Create a Branch**: Create a new branch for your contribution.

    ```bash
    git checkout -b feature/your-feature
    ```

4. **Make Changes**: Make your changes, and ensure that your code adheres to our coding standards and follows best practices. Please.. Please.. Please.. take care of following PEP8, and code level documentation. READ [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)

5. **Confirm Rebase**: Make sure your branch is rebased to the latest master.
   ```bash
   git fetch --all
   git checkout master
   git pull origin master
   git checkout feature/your-feature
   git rebase master
   ```
   
6. **Commit Changes**: Commit your changes with a clear and concise message.

    ```bash
    git commit -m "Add feature/fix for Django SSO Engine"
    ```

7. **Push Changes**: Push your changes to your fork on GitHub.
    
    ```bash
    git push origin feature/your-feature
    ```
   
8. **Submit a Pull Request**: Open a pull request to the original repository. Make sure to provide a detailed description of your changes.

9. **Review and Discuss**: Participate in the discussion on your pull request. Make any necessary adjustments based on feedback.

10. **Squash Commits**: If your pull request requires multiple commits, squash them into a single commit for a cleaner history.

11. **Merge**: Once your pull request is approved and passes all checks, it will be merged into the main project.


## Reporting Issues
If you find a bug or have a suggestion, please open an issue on the Django SSO Engine GitHub issue tracker. Make sure to provide a clear and detailed description of the issue or feature request.

## License
By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

Thank you for contributing to Django SSO Engine!

Django SSO Engine - A powerful Single Sign-On (SSO) engine for Django for your startup Organization.


