const fs = require('fs')
const _ = require('lodash')

const fontFileNames = () => {
  const array = fs
    .readdirSync('assets/fonts')
    .map(file => file.replace('.ttf', '').replace('.otf', ''))
  return Array.from(new Set(array))
}
const generate = () => {
  const properties = fontFileNames()
    .map(name => `${_.camelCase(name.replace('.otf', '').replace(/-/g, '').replace(/\s/g, ''))}: '${name.replace('Ubuntu-Regular', 'Ubuntu')}'`)
    .join(',\n  ')
  const string = `// DO NOT MODIFY THIS FILE
// It is autogenerated when running "yarn run fonts" and will
// generate font references for all fonts located in "src/res/fonts"

const fonts = {
  ${properties}
}
export default fonts
`
  fs.writeFileSync('assets/fonts.js', string, 'utf8')
}
generate()
