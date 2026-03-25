import { Hono } from 'hono';
import { supabase } from '../lib/supabase.js';
import { generateReply } from '../lib/anthropic.js';
import { sendReplyEmail } from '../lib/resend.js';
import type { LeadPayload } from '../types.js';

export const webhookRouter = new Hono();

webhookRouter.post('/', async (c) => {
  let body: LeadPayload;

  try {
    body = await c.req.json<LeadPayload>();
  } catch {
    return c.json({ error: 'Neplatné JSON tělo požadavku' }, 400);
  }

  const { name, email, message } = body;

  if (!name || !email || !message) {
    return c.json({ error: 'Chybí povinná pole: name, email, message' }, 400);
  }

  // 1. Uložení leadu do Supabase
  const { data, error: dbError } = await supabase
    .from('leads')
    .insert({ name, email, message })
    .select('id')
    .single();

  if (dbError) {
    console.error('Chyba při ukládání do Supabase:', dbError);
    return c.json({ error: 'Nepodařilo se uložit lead' }, 500);
  }

  // 2. Vygenerování odpovědi pomocí Anthropic AI
  let reply: string;
  try {
    reply = await generateReply(message);
  } catch (err) {
    console.error('Chyba Anthropic API:', err);
    return c.json({ error: 'Nepodařilo se vygenerovat odpověď' }, 500);
  }

  // 3. Odeslání emailu přes Resend
  try {
    await sendReplyEmail(email, name, reply);
  } catch (err) {
    console.error('Chyba při odesílání emailu:', err);
    return c.json({ error: 'Nepodařilo se odeslat email' }, 500);
  }

  // 4. Uložení vygenerované odpovědi do DB
  await supabase.from('leads').update({ reply }).eq('id', data.id);

  return c.json({ success: true, id: data.id, reply }, 201);
});
