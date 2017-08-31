s/ \([a-z]'\) / \1/g
s/\([A-Z]'\) /\1/g
s/ "\([a-z]'\) / \1/g
s/ (\([a-z]'\) / \1/g
s/^\([a-z]'\) /\1/g
# remove first to letter to handle upper/lower case
s/ qu' / qu'/g
s/ujourd' hui/ujourd'hui/g
# jusqu' puisqu' quoiqu' quelqu'
s/usqu' /usque'/g
s/uisqu' /uisque'/g
s/uoiqu' /uoique'/g
s/orsqu' /orsque'/g
s/uelqu' /uelque'/g
#
s/Qu' /Qu'/g
#
s/d' uvre/d'oeuvre/g
s/d' oeuvre/d'oeuvre/g
