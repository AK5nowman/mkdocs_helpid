# Summary
Mkdocs hook to generate a redirection `Default.htm` page to map from a `cshid` to a page or section reference. Target use is to generate custom help documentation to be used with [VTScada custom help](https://www.vtscada.com/help/Content/D_Customize/Dev_CustomHelpFiles.htm)

This is a proof of concept, has not been proven in production.

# How To Use
Each `helpid` needs to be an interger and globally unique. Last entry wins, but a warning will be issued during build.

## Page Reference
Simply add a line to the page meta data defining the help id
```html
---
helpid: 100
---

# Summary
etc..
```
## Section Reference
A `helpid` can be assosciated with any level of heading.
```html
# My Section { helpid: 101 }
## Level 2 { helpid: 102 }
### Level 3 { helpid: 103 }
#### Level 4 { helpid: 104 }
##### Level 5 { helpid: 105 }
###### Level 6 { helpid: 106 }

```

## Together
This will map `100 => mypage.html`, `101 => mypage.html#summary`, and `102 => mypage.html#review`. No `helpid` will reference the Body section.
```html
---
helpid: 100
---

# Summary { helpid: 101 }
Here is what the content will be

# Body 
Here is the main content.

# Review { helpid: 102 }
And that is the content
```