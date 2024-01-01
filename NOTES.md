```xml
<Request>
    <Login>
        <Username>{{username}}</Username>
        <Password>{{password}}</Password>
    </Login>
    <Get>
        <WirelessNetworkStatus>
        </WirelessNetworkStatus>
    </Get>
</Request>




<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.2" IPS_CAT_VER="0">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <WirelessNetworkStatus transactionid="">
        <Name>GuestAP</Name>
        <Status>Enable</Status>
    </WirelessNetworkStatus>
    <WirelessNetworkStatus transactionid="">
        <Name>Sophos</Name>
        <Status>Enable</Status>
    </WirelessNetworkStatus>
</Response>



<Request>
    <Login>
        <Username>{{username}}</Username>
        <Password>{{password}}</Password>
    </Login>
    <Remove>
    <WirelessNetworks transactionid="">
        <Name>Sophos</Name>
    </WirelessNetworks>
    </Remove>
</Request>




<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.2" IPS_CAT_VER="0">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <WirelessNetworks transactionid="">
        <Status code="200">Configuration applied successfully.</Status>
    </WirelessNetworks>
</Response>




<Request>
    <Login>
        <Username>{{username}}</Username>
        <Password>{{password}}</Password>
    </Login>
    <Set>
      <WirelessProtectionGlobalSettings>
        <EnableWirelessProtection>Disable</EnableWirelessProtection>
        <AllowedZone>
        </AllowedZone>
        <RADIUSServer>None</RADIUSServer>
      </WirelessProtectionGlobalSettings>
    </Set>
</Request>






-------



<Request>
    <Login>
        <Username>{{username}}</Username>
        <Password>{{password}}</Password>
    </Login>
    <Get>
        <FirewallRule >
        </FirewallRule >
    </Get>
</Request>



<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1905.1" IPS_CAT_VER="0">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <FirewallRule transactionid="">
        <Name>[example] Traffic to Internal Zones</Name>
        <Description>A disabled Firewall rule with the destination zone as LAN, WiFi, VPN or DMZ . Such rules would be added to Traffic to Internal Zones group on the first match basis if user selects automatic grouping option.</Description>
        <IPFamily>IPv4</IPFamily>
        <Status>Disable</Status>
        <Position>Top</Position>
        <PolicyType>User</PolicyType>
        <UserPolicy>
            <Action>Drop</Action>
            <LogTraffic>Enable</LogTraffic>
            <DestinationZones>
                <Zone>LAN</Zone>
                <Zone>DMZ</Zone>
                <Zone>VPN</Zone>
                <Zone>WiFi</Zone>
            </DestinationZones>
            <Schedule>All The Time</Schedule>
            <SkipLocalDestined>Disable</SkipLocalDestined>
            <MatchIdentity>Enable</MatchIdentity>
            <DataAccounting>Disable</DataAccounting>
            <ShowCaptivePortal>Enable</ShowCaptivePortal>
        </UserPolicy>
    </FirewallRule>
    <FirewallRule transactionid="">
        <Name>[example] Traffic to WAN</Name>
        <Description>A disabled Firewall rule with the destination zone as WAN. Such rules would be added to Traffic to WAN group on the first match basis if user selects automatic grouping option.</Description>
        <IPFamily>IPv4</IPFamily>
        <Status>Disable</Status>
        <Position>After</Position>
        <PolicyType>Network</PolicyType>
        <After>
            <Name>[example] Traffic to Internal Zones</Name>
        </After>
        <NetworkPolicy>
            <Action>Drop</Action>
            <LogTraffic>Enable</LogTraffic>
            <SkipLocalDestined>Disable</SkipLocalDestined>
            <DestinationZones>
                <Zone>WAN</Zone>
            </DestinationZones>
            <Schedule>All The Time</Schedule>
        </NetworkPolicy>
    </FirewallRule>
    <FirewallRule transactionid="">
        <Name>[example] Traffic to DMZ</Name>
        <Description>A disabled Firewall rule with the destination zone as DMZ. Such rules would be added to Traffic to DMZ group on the first match basis if user selects automatic grouping option.</Description>
        <IPFamily>IPv4</IPFamily>
        <Status>Disable</Status>
        <Position>After</Position>
        <PolicyType>User</PolicyType>
        <After>
            <Name>[example] Traffic to WAN</Name>
        </After>
        <UserPolicy>
            <Action>Drop</Action>
            <LogTraffic>Enable</LogTraffic>
            <DestinationZones>
                <Zone>DMZ</Zone>
            </DestinationZones>
            <Schedule>All The Time</Schedule>
            <SkipLocalDestined>Disable</SkipLocalDestined>
            <MatchIdentity>Enable</MatchIdentity>
            <DataAccounting>Disable</DataAccounting>
            <ShowCaptivePortal>Enable</ShowCaptivePortal>
        </UserPolicy>
    </FirewallRule>
    <FirewallRule transactionid="">
        <Name>Auto added firewall policy for MTA</Name>
        <Description>This rule was added automatically by SFOS MTA. However you could edit this policy based on network requirement.</Description>
        <IPFamily>IPv4</IPFamily>
        <Status>Enable</Status>
        <Position>After</Position>
        <PolicyType>Network</PolicyType>
        <After>
            <Name>[example] Traffic to DMZ</Name>
        </After>
        <NetworkPolicy>
            <Action>Accept</Action>
            <LogTraffic>Disable</LogTraffic>
            <SkipLocalDestined>Disable</SkipLocalDestined>
            <Schedule>All The Time</Schedule>
            <Services>
                <Service>SMTP</Service>
                <Service>SMTP(S)</Service>
            </Services>
            <DSCPMarking>-1</DSCPMarking>
            <WebFilter>None</WebFilter>
            <WebCategoryBaseQoSPolicy> </WebCategoryBaseQoSPolicy>
            <BlockQuickQuic>Disable</BlockQuickQuic>
            <ScanVirus>Disable</ScanVirus>
            <ZeroDayProtection>Disable</ZeroDayProtection>
            <ProxyMode>Disable</ProxyMode>
            <DecryptHTTPS>Disable</DecryptHTTPS>
            <ApplicationControl>None</ApplicationControl>
            <ApplicationBaseQoSPolicy> </ApplicationBaseQoSPolicy>
            <IntrusionPrevention>None</IntrusionPrevention>
            <TrafficShappingPolicy>None</TrafficShappingPolicy>
            <ScanSMTP>Enable</ScanSMTP>
            <ScanSMTPS>Enable</ScanSMTPS>
            <ScanIMAP>Disable</ScanIMAP>
            <ScanIMAPS>Disable</ScanIMAPS>
            <ScanPOP3>Disable</ScanPOP3>
            <ScanPOP3S>Disable</ScanPOP3S>
            <ScanFTP>Disable</ScanFTP>
            <SourceSecurityHeartbeat>Disable</SourceSecurityHeartbeat>
            <MinimumSourceHBPermitted>No Restriction</MinimumSourceHBPermitted>
            <DestSecurityHeartbeat>Disable</DestSecurityHeartbeat>
            <MinimumDestinationHBPermitted>No Restriction</MinimumDestinationHBPermitted>
        </NetworkPolicy>
    </FirewallRule>
</Response>
```
