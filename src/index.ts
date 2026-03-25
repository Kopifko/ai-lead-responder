import 'dotenv/config';
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { webhookRouter } from './routes/webhook.js';

const app = new Hono();

app.route('/api/webhook', webhookRouter);

app.get('/health', (c) => c.json({ status: 'ok' }));

const port = Number(process.env.PORT) || 3000;

serve({ fetch: app.fetch, port }, () => {
  console.log(`Server running on http://localhost:${port}`);
});
