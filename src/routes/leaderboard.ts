import { Hono } from 'hono';
import { supabase } from '../lib/supabase.js';

export const leaderboardRouter = new Hono();

// GET /api/leaderboard — vrátí top 10 skóre
leaderboardRouter.get('/', async (c) => {
  const { data, error } = await supabase
    .from('scores')
    .select('id, name, score, created_at')
    .order('score', { ascending: false })
    .limit(10);

  if (error) {
    console.error('Chyba při načítání žebříčku:', error);
    return c.json({ error: 'Nepodařilo se načíst žebříček' }, 500);
  }

  return c.json({ scores: data });
});

// POST /api/leaderboard — uložení skóre { name, score }
leaderboardRouter.post('/', async (c) => {
  let body: { name?: unknown; score?: unknown };
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: 'Neplatné JSON tělo' }, 400);
  }

  const name  = typeof body.name  === 'string' ? body.name.trim()       : null;
  const score = typeof body.score === 'number' ? Math.floor(body.score) : null;

  if (!name || name.length < 1 || name.length > 32)
    return c.json({ error: 'Neplatné jméno (1–32 znaků)' }, 400);
  if (score === null || score < 0)
    return c.json({ error: 'Neplatné skóre' }, 400);

  const { data, error } = await supabase
    .from('scores')
    .insert({ name, score })
    .select('id, name, score')
    .single();

  if (error) {
    console.error('Chyba při ukládání skóre:', error);
    return c.json({ error: 'Nepodařilo se uložit skóre' }, 500);
  }

  return c.json({ success: true, entry: data }, 201);
});
