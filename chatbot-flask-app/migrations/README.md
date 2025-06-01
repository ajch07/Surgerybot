# Database Migrations for Chatbot Flask App

This directory contains the migration files for the Chatbot Flask application. Migrations are essential for managing changes to the database schema over time.

## Getting Started with Migrations

To handle database migrations, you can use a migration tool like Flask-Migrate, which is built on top of Alembic. Follow the steps below to set up and manage your migrations:

1. **Install Flask-Migrate**: Ensure that Flask-Migrate is included in your `requirements.txt` file. If not, add it:
   ```
   Flask-Migrate
   ```

2. **Initialize Migrations**: Run the following command to initialize the migration repository:
   ```
   flask db init
   ```

3. **Create a Migration**: Whenever you make changes to your models, create a new migration file using:
   ```
   flask db migrate -m "Description of changes"
   ```

4. **Apply Migrations**: To apply the migrations to your database, run:
   ```
   flask db upgrade
   ```

5. **Downgrade Migrations**: If you need to revert to a previous migration, you can use:
   ```
   flask db downgrade
   ```

## Best Practices

- Always review the generated migration scripts before applying them to ensure they accurately reflect your intended changes.
- Keep your migrations organized and descriptive to make it easier to track changes over time.
- Regularly back up your database, especially before applying new migrations.

For more detailed information on using Flask-Migrate and Alembic, refer to the official documentation.