import nodemailer from 'nodemailer';

const gmailUser = process.env.GMAIL_USER;
const gmailAppPassword = process.env.GMAIL_APP_PASSWORD;

if (!gmailUser || !gmailAppPassword) {
  throw new Error('Missing GMAIL_USER or GMAIL_APP_PASSWORD environment variables');
}

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 465,
  secure: true,
  family: 4,
  auth: {
    user: gmailUser,
    pass: gmailAppPassword,
  },
});

export async function sendReplyEmail(to: string, name: string, reply: string): Promise<void> {
  const companyName = process.env.COMPANY_NAME || 'Naše společnost';
  const contactName = process.env.CONTACT_NAME || '';
  const contactPhone = process.env.CONTACT_PHONE || '';
  const contactWeb = process.env.CONTACT_WEB || '';

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

  await transporter.sendMail({
    from: `${companyName} <${gmailUser}>`,
    to,
    subject: `Děkujeme za váš zájem, ${name}!`,
    text: `${reply}\n\n${signature}`,
    html: `<p>${reply.replace(/\n/g, '<br/>')}</p>${htmlSignature}`,
  });
}
