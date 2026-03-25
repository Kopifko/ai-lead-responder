import { Resend } from 'resend';

const apiKey = process.env.RESEND_API_KEY;

if (!apiKey) {
  throw new Error('Missing RESEND_API_KEY environment variable');
}

export const resendClient = new Resend(apiKey);

export async function sendReplyEmail(to: string, name: string, reply: string): Promise<void> {
  const companyName = process.env.COMPANY_NAME || 'Naše společnost';
  const contactName = process.env.CONTACT_NAME || '';
  const contactPhone = process.env.CONTACT_PHONE || '';
  const contactWeb = process.env.CONTACT_WEB || '';
  const fromEmail = process.env.FROM_EMAIL || 'onboarding@resend.dev';

  const signature = `
--
${contactName ? contactName + '\n' : ''}${companyName}${contactPhone ? '\nTel: ' + contactPhone : ''}${contactWeb ? '\nWeb: ' + contactWeb : ''}
  `.trim();

  const htmlSignature = `
    <br/><br/>
    <hr style="border:none;border-top:1px solid #eee;margin:20px 0"/>
    <p style="color:#666;font-size:13px;margin:0">
      ${contactName ? `<strong>${contactName}</strong><br/>` : ''}
      ${companyName}<br/>
      ${contactPhone ? `Tel: ${contactPhone}<br/>` : ''}
      ${contactWeb ? `Web: <a href="https://${contactWeb}">${contactWeb}</a>` : ''}
    </p>
  `;

  const { error } = await resendClient.emails.send({
    from: `${companyName} <${fromEmail}>`,
    to,
    subject: `Děkujeme za váš zájem, ${name}!`,
    text: `${reply}\n\n${signature}`,
    html: `<p>${reply.replace(/\n/g, '<br/>')}</p>${htmlSignature}`,
  });

  if (error) {
    throw new Error(`Resend email error: ${error.message}`);
  }
}
