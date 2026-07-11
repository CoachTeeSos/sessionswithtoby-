
const fs = require('fs');
const { execSync } = require('child_process');

const html = fs.readFileSync('index.html', 'utf8');
const scriptStart = html.indexOf('<script>') + 8;
const scriptEnd = html.lastIndexOf('</script>');
const js = html.slice(scriptStart, scriptEnd);

fs.writeFileSync('/tmp/check.js', js);
try {
  execSync('node --check /tmp/check.js', { stdio: 'ignore' });
  console.log('✅ JS syntax valid');
} catch (e) {
  console.error('❌ JS syntax error:', e.stderr.toString());
  process.exit(1);
}
