# Milwaukee Metropolitan Sewerage District Parser for Home Assistant

Adds MMSD Deep Tunnel and water treatment plant capacities to Home Assistant.

### Installation 

Install [HACS](https://www.hacs.xyz/)

Navigate to `HACS` in your Home Assistant 

Add https://github.com/jasonfry89/homeassistant-milwaukee-mmsd as a [Custom Repository](https://www.hacs.xyz/docs/faq/custom_repositories/) as type `Integration`

Search HACS for `Milwaukee Metropolitan Sewerage District` and click `Download`

Restart Home Assistant

Navigate to `Integrations`

Press `Add integration`

Search for `Milwaukee Metropolitan Sewerage District`

### Developing

Follow the instructions [here](https://developers.home-assistant.io/docs/development_environment/) to setup a local Home Assistant development environment

Modify `$YOUR_HA_DEV_ENV/homeassistant/generated/integrations.json` to include:

```
"milwaukee_mmsd_parser": {
  "name": "Milwaukee Metropolitan Sewerage District",
  "integration_type": "service",
  "config_flow": true,
  "iot_class": "cloud_polling"
},
```

Create a symbolic link to this repository:

`ln -s $THIS_REPO/custom_components/milwaukee_mmsd_parser $YOUR_HA_DEV_ENV/homeassistant/components/milwaukee_mmsd_parser`

This approach allows you to test your code in the development environment and get syntax highlighting