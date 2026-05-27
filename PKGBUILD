# Maintainer: 1mesles1 <https://github.com/1mesles1>
pkgname=hotkeyhelper-git
pkgver=1.0.0
pkgrel=1
pkgdesc="A lightweight, adaptive hotkey cheat sheet for tiling window managers (i3wm, sway)"
arch=('any')
url="https://github.com/1mesles1/hotkeyhelper"
license=('GPL3')
depends=('python')
makedepends=('git')
provides=('hotkeyhelper')
conflicts=('hotkeyhelper')
source=("git+${url}.git")
md5sums=('SKIP')

package() {
    cd "${srcdir}/hotkeyhelper"
    install -d "${pkgdir}/usr/bin"
    install -d "${pkgdir}/usr/share/doc/hotkeyhelper"
    install -m755 main.py "${pkgdir}/usr/bin/hotkeyhelper"
    install -m644 README.md "${pkgdir}/usr/share/doc/hotkeyhelper/README.md"
}


