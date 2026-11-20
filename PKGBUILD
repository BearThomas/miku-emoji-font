# Maintainer: Thomas <thomas_xiong@outlook.com>
pkgname=ttf-miku-emoji
pkgver=2.0.0
pkgrel=1
pkgdesc="Fan-made chibi Hatsune Miku color emoji font (38 emoji, CBDT/CBLC)"
arch=('any')
url="https://github.com/BearThomas/miku-emoji-font"
license=('custom:Piapro-Character-License')
install="$pkgname.install"
provides=('miku-emoji-font')
conflicts=('miku-emoji-font')
source=("MikuEmoji.ttf" "75-miku-emoji.conf" "LICENSE" "README.md")
sha256sums=('084ae6241b45ac9ed35ec67d9203d60714e64fa6a40201287ea76005421f5e20'
            'SKIP' 'SKIP' 'SKIP')

package() {
  install -Dm644 MikuEmoji.ttf "$pkgdir/usr/share/fonts/miku-emoji/MikuEmoji.ttf"
  install -Dm644 75-miku-emoji.conf "$pkgdir/usr/share/fontconfig/conf.avail/75-miku-emoji.conf"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
  # conf is NOT enabled by default - see .install for opt-in instructions
}
