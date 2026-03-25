import { Resend } from 'resend';

const apiKey = process.env.RESEND_API_KEY;

if (!apiKey) {
  throw new Error('Missing RESEND_API_KEY environment variable');
}

export const resendClient = new Resend(apiKey);

export async function sendReplyEmail(to: string, name: string, reply: string): Promise<void> {
  const { error } = await resendClient.emails.send({
    from: 'AI Lead Responder <onboarding@resend.dev>',
    to,
    subject: `Děkujeme za váš zájem, ${name}!`,
    text: reply,
  });

  if (error) {
    throw new Error(`Resend email error: ${error.message}`);
  }
}
