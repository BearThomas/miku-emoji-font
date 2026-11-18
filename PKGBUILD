# Maintainer: Thomas <thomas_xiong@outlook.com>
pkgname=ttf-miku-emoji
pkgver=1.5.0
pkgrel=1
pkgdesc="Fan-made chibi Hatsune Miku color emoji font (38 emoji, CBDT/CBLC)"
arch=('any')
url="https://github.com/BearThomas/miku-emoji-font"
license=('custom:Piapro-Character-License')
install="$pkgname.install"
provides=('miku-emoji-font')
conflicts=('miku-emoji-font')
source=("MikuEmoji.ttf" "75-miku-emoji.conf" "LICENSE" "README.md")
sha256sums=('bda73960212062fa3571cd3c78b3c08de3296a643a7db424751fd65b8f53588b'
            'SKIP' 'SKIP' 'SKIP')

package() {
  install -Dm644 MikuEmoji.ttf "$pkgdir/usr/share/fonts/miku-emoji/MikuEmoji.ttf"
  install -Dm644 75-miku-emoji.conf "$pkgdir/usr/share/fontconfig/conf.avail/75-miku-emoji.conf"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
  install -d "$pkgdir/etc/fonts/conf.d"
  ln -s /usr/share/fontconfig/conf.avail/75-miku-emoji.conf "$pkgdir/etc/fonts/conf.d/75-miku-emoji.conf"
}
