#!/bin/bash
token=""
uuid=""
#curl -H "Authorization: Bearer $me" https://api.starlingbank.com/api/v2/accounts/
curl -s -H "Authorization: Bearer $token" https://api.starlingbank.com/api/v2/accounts/$uuid/balance | python -m json.tool | grep -A2 effectiveBalance | grep minorUnits | cut -c23- | xargs -I {} echo "scale=2; {}  / 100.0" | bc -l
