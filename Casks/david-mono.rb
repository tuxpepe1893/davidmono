cask "david-mono" do
  version "1.0.2"
  sha256 "ee814f604d7f439af3062f2a61454237a1999624f6c28299aa672f3391b5d93e"

  url "https://github.com/tuxpepe1893/davidmono/releases/download/v#{version}/DavidMono-#{version}.zip"
  name "David Mono"
  desc "Monospaced JetBrains Mono for Latin with proportional Noto Sans Hebrew"
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
