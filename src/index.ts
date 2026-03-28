import 'dotenv/config';
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { webhookRouter } from './routes/webhook.js';
import { leaderboardRouter } from './routes/leaderboard.js';

const app = new Hono();

app.use('*', cors());

app.route('/api/webhook', webhookRouter);
app.route('/api/leaderboard', leaderboardRouter);

app.get('/health', (c) => c.json({ status: 'ok' }));

const port = Number(process.env.PORT) || 3000;

serve({ fetch: app.fetch, port, hostname: '0.0.0.0' }, () => {
  console.log(`Server running on http://localhost:${port}`);
});
