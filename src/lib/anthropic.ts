import Groq from 'groq-sdk';

const apiKey = process.env.GROQ_API_KEY;

if (!apiKey) {
  throw new Error('Missing GROQ_API_KEY environment variable');
}

const groq = new Groq({ apiKey });

export async function generateReply(message: string): Promise<string> {
  const response = await groq.chat.completions.create({
    model: 'llama-3.3-70b-versatile',
    messages: [
      {
        role: 'user',
        content: `Jsi asistent pro zákaznický servis. Zákazník nám poslal tuto zprávu:\n\n"${message}"\n\nNapiš zdvořilou, profesionální odpověď v češtině, která zákazníka pozdraví, poděkuje za zájem a zeptá se na jeho budget (rozpočet) a timeline (časový plán projektu). Odpověď by měla být stručná (3-4 věty).`,
      },
    ],
  });

  return response.choices[0].message.content ?? '';
}
