/* docs/javascripts/svg-panzoom-init.js */
function enableSvgPanZoom() {
  document.querySelectorAll('svg.dag').forEach(svg => {
    // don’t double-init when navigating with “instant loading”
    if (!svg.__panZoomInstance) {
      svg.__panZoomInstance = svgPanZoom(svg, {
        controlIconsEnabled: true,
      });
    }
  });
}

enableSvgPanZoom();               // first page load

/* Material for MkDocs swaps page bodies without a full reload,
   so hook into its document$ observable to re-run the setup */
if (typeof window.document$ !== "undefined") {
  document$.subscribe(enableSvgPanZoom);   //   ← official callback point:contentReference[oaicite:1]{index=1}
}
