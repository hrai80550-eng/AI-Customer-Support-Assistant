# AI Customer Support Assistant

## Render deployment

The repository includes a `render.yaml` Blueprint that creates separate Flask
and Rasa web services. Create a new Blueprint in Render and connect this GitHub
repository.

The Flask application uses SQLite. On Render's free plan, the database file is
ephemeral and can be reset during a restart or deployment. For persistent data,
upgrade the Flask service, attach a disk at `/var/data`, and set:

```text
DATABASE_PATH=/var/data/customer_support_chatbot.db
```

If Render changes either generated service name, update the Flask service's
`RASA_URL` environment variable to the public URL of the Rasa service.
