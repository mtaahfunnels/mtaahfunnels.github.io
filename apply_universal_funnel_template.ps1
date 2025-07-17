# C:\Users\myeku\clicksites_funnels\apply_universal_funnel_template.ps1
# 🔁 Auto-patches all thankyou.html files inside /funnels/*/ with universal thank you logic
# 💡 Make sure funnel_server.py is running to serve /api/funnel-assets/<slug>

$rootPath = "$PSScriptRoot\funnels"
$thankYouCode = @'
<!-- UNIVERSAL THANK YOU INJECT -->
<script>
  (function(){
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get("name") || "Friend";
    const slugParts = window.location.pathname.split("/");
    const slug = slugParts.includes("funnels") ? slugParts[slugParts.indexOf("funnels") + 1] : "default";

    const heading = document.getElementById("thankyou-heading");
    const subtext = document.getElementById("subtext");

    if (heading) heading.textContent = `Thank you, ${name}!`;
    if (subtext) subtext.textContent = `We've sent your guide to the email you provided, ${name}.`;

    fetch(`/api/funnel-assets/${slug}`)
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("asset-blocks");
        const assets = data.assets || data;

        if (!container) return;

        if (assets.image) {
          const img = document.createElement("img");
          img.src = assets.image;
          img.alt = "Guide Image";
          img.style = "max-width:100%;margin-bottom:20px;border-radius:8px;";
          container.appendChild(img);
        }

        if (assets.pdf) {
          const link = document.createElement("a");
          link.href = assets.pdf;
          link.textContent = "📘 Download PDF Guide";
          link.className = "cta-link";
          container.appendChild(link);
        }

        if (assets.video_url) {
          const vid = document.createElement("a");
          vid.href = assets.video_url;
          vid.textContent = "▶️ Watch the Video";
          vid.className = "cta-link";
          container.appendChild(vid);
        }

        if (assets.external_link) {
          const ext = document.createElement("a");
          ext.href = assets.external_link;
          ext.textContent = "🔗 Visit Website";
          ext.className = "cta-link";
          container.appendChild(ext);
        }
      })
      .catch(err => console.error("Failed to load funnel assets:", err));
  })();
</script>
<!-- END UNIVERSAL THANK YOU INJECT -->
'@

Get-ChildItem -Path $rootPath -Recurse -Filter "thankyou.html" | ForEach-Object {
    Write-Host "✅ Updating: $($_.FullName)"

    $html = Get-Content $_.FullName -Raw
    $pattern = '<!-- UNIVERSAL THANK YOU INJECT -->[\s\S]*?<!-- END UNIVERSAL THANK YOU INJECT -->'

    if ($html -match $pattern) {
        $html = [System.Text.RegularExpressions.Regex]::Replace($html, $pattern, $thankYouCode)
    } else {
        $html = $html -replace '</body>', "$thankYouCode`r`n</body>"
    }

    Set-Content $_.FullName -Value $html -Encoding UTF8
    Write-Host "✨ Injected thank you logic into $($_.BaseName)\thankyou.html"
}
