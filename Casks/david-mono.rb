cask "david-mono" do
  version "1.0.1"
  sha256 "ddc357b795b5bdf9778328b639c73b41f67958faba041a3b06128867a259917a"

  url "https://github.com/tuxpepe1893/davidmono/releases/download/v#{version}/DavidMono-#{version}.zip"
  name "David Mono"
  desc "JetBrains Mono for Latin with Noto Sans Hebrew in one monospaced family"
  homepage "https://github.com/tuxpepe1893/davidmono"

  livecheck do
    url :url
    strategy :github_latest
  end

  font "DavidMono-#{version}/ttf/DavidMono-Bold.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-BoldItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-ExtraBold.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-ExtraBoldItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-ExtraLight.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-ExtraLightItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-Italic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-Light.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-LightItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-Medium.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-MediumItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-Regular.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-SemiBold.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-SemiBoldItalic.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-Thin.ttf"
  font "DavidMono-#{version}/ttf/DavidMono-ThinItalic.ttf"
end
