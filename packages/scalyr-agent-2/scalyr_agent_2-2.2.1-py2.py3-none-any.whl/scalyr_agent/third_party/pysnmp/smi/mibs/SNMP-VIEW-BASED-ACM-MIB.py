#
# PySNMP MIB module SNMP-VIEW-BASED-ACM-MIB (http://pysnmp.sf.net)
# ASN.1 source file:///usr/share/snmp/mibs/SNMP-VIEW-BASED-ACM-MIB.txt
# Produced by pysmi-0.0.5 at Sat Sep 19 23:12:54 2015
# On host grommit.local platform Darwin version 14.4.0 by user ilya
# Using Python version 2.7.6 (default, Sep  9 2014, 15:04:36) 
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( SnmpSecurityModel, SnmpAdminString, SnmpSecurityLevel, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpSecurityModel", "SnmpAdminString", "SnmpSecurityLevel")
( NotificationGroup, ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
( Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, ModuleIdentity, Gauge32, snmpModules, iso, ObjectIdentity, Bits, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "ModuleIdentity", "Gauge32", "snmpModules", "iso", "ObjectIdentity", "Bits", "Counter32")
( StorageType, DisplayString, RowStatus, TextualConvention, TestAndIncr, ) = mibBuilder.importSymbols("SNMPv2-TC", "StorageType", "DisplayString", "RowStatus", "TextualConvention", "TestAndIncr")
snmpVacmMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 16)).setRevisions(("2002-10-16 00:00", "1999-01-20 00:00", "1997-11-20 00:00",))
if mibBuilder.loadTexts: snmpVacmMIB.setLastUpdated('200210160000Z')
if mibBuilder.loadTexts: snmpVacmMIB.setOrganization('SNMPv3 Working Group')
if mibBuilder.loadTexts: snmpVacmMIB.setContactInfo('WG-email:   snmpv3@lists.tislabs.com\n                  Subscribe:  majordomo@lists.tislabs.com\n                              In message body:  subscribe snmpv3\n\n                  Co-Chair:   Russ Mundy\n                              Network Associates Laboratories\n                  postal:     15204 Omega Drive, Suite 300\n                              Rockville, MD 20850-4601\n                              USA\n                  email:      mundy@tislabs.com\n                  phone:      +1 301-947-7107\n\n                  Co-Chair:   David Harrington\n                              Enterasys Networks\n                  Postal:     35 Industrial Way\n                              P. O. Box 5004\n                              Rochester, New Hampshire 03866-5005\n                              USA\n                  EMail:      dbh@enterasys.com\n                  Phone:      +1 603-337-2614\n\n                  Co-editor:  Bert Wijnen\n                              Lucent Technologies\n                  postal:     Schagen 33\n                              3461 GL Linschoten\n                              Netherlands\n                  email:      bwijnen@lucent.com\n                  phone:      +31-348-480-685\n\n                  Co-editor:  Randy Presuhn\n                              BMC Software, Inc.\n\n                  postal:     2141 North First Street\n                              San Jose, CA 95131\n                              USA\n                  email:      randy_presuhn@bmc.com\n                  phone:      +1 408-546-1006\n\n                  Co-editor:  Keith McCloghrie\n                              Cisco Systems, Inc.\n                  postal:     170 West Tasman Drive\n                              San Jose, CA  95134-1706\n                              USA\n                  email:      kzm@cisco.com\n                  phone:      +1-408-526-5260\n                 ')
if mibBuilder.loadTexts: snmpVacmMIB.setDescription('The management information definitions for the\n                  View-based Access Control Model for SNMP.\n\n                  Copyright (C) The Internet Society (2002). This\n                  version of this MIB module is part of RFC 3415;\n                  see the RFC itself for full legal notices.\n                 ')
vacmMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 16, 1))
vacmMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 16, 2))
vacmContextTable = MibTable((1, 3, 6, 1, 6, 3, 16, 1, 1), )
if mibBuilder.loadTexts: vacmContextTable.setDescription('The table of locally available contexts.\n\n                 This table provides information to SNMP Command\n\n                 Generator applications so that they can properly\n                 configure the vacmAccessTable to control access to\n                 all contexts at the SNMP entity.\n\n                 This table may change dynamically if the SNMP entity\n                 allows that contexts are added/deleted dynamically\n                 (for instance when its configuration changes).  Such\n                 changes would happen only if the management\n                 instrumentation at that SNMP entity recognizes more\n                 (or fewer) contexts.\n\n                 The presence of entries in this table and of entries\n                 in the vacmAccessTable are independent.  That is, a\n                 context identified by an entry in this table is not\n                 necessarily referenced by any entries in the\n                 vacmAccessTable; and the context(s) referenced by an\n                 entry in the vacmAccessTable does not necessarily\n                 currently exist and thus need not be identified by an\n                 entry in this table.\n\n                 This table must be made accessible via the default\n                 context so that Command Responder applications have\n                 a standard way of retrieving the information.\n\n                 This table is read-only.  It cannot be configured via\n                 SNMP.\n                ')
vacmContextEntry = MibTableRow((1, 3, 6, 1, 6, 3, 16, 1, 1, 1), ).setIndexNames((0, "SNMP-VIEW-BASED-ACM-MIB", "vacmContextName"))
if mibBuilder.loadTexts: vacmContextEntry.setDescription('Information about a particular context.')
vacmContextName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 1, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,32))).setMaxAccess("readonly")
if mibBuilder.loadTexts: vacmContextName.setDescription('A human readable name identifying a particular\n                 context at a particular SNMP entity.\n\n                 The empty contextName (zero length) represents the\n                 default context.\n                ')
vacmSecurityToGroupTable = MibTable((1, 3, 6, 1, 6, 3, 16, 1, 2), )
if mibBuilder.loadTexts: vacmSecurityToGroupTable.setDescription('This table maps a combination of securityModel and\n                 securityName into a groupName which is used to define\n                 an access control policy for a group of principals.\n                ')
vacmSecurityToGroupEntry = MibTableRow((1, 3, 6, 1, 6, 3, 16, 1, 2, 1), ).setIndexNames((0, "SNMP-VIEW-BASED-ACM-MIB", "vacmSecurityModel"), (0, "SNMP-VIEW-BASED-ACM-MIB", "vacmSecurityName"))
if mibBuilder.loadTexts: vacmSecurityToGroupEntry.setDescription('An entry in this table maps the combination of a\n                 securityModel and securityName into a groupName.\n                ')
vacmSecurityModel = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 2, 1, 1), SnmpSecurityModel().subtype(subtypeSpec=ValueRangeConstraint(1,2147483647)))
if mibBuilder.loadTexts: vacmSecurityModel.setDescription("The Security Model, by which the vacmSecurityName\n                 referenced by this entry is provided.\n\n                 Note, this object may not take the 'any' (0) value.\n                ")
vacmSecurityName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 2, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1,32)))
if mibBuilder.loadTexts: vacmSecurityName.setDescription('The securityName for the principal, represented in a\n                 Security Model independent format, which is mapped by\n                 this entry to a groupName.\n                ')
vacmGroupName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 2, 1, 3), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1,32))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmGroupName.setDescription('The name of the group to which this entry (e.g., the\n                 combination of securityModel and securityName)\n                 belongs.\n\n                 This groupName is used as index into the\n                 vacmAccessTable to select an access control policy.\n                 However, a value in this table does not imply that an\n                 instance with the value exists in table vacmAccesTable.\n                ')
vacmSecurityToGroupStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 2, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmSecurityToGroupStorageType.setDescription("The storage type for this conceptual row.\n                 Conceptual rows having the value 'permanent' need not\n                 allow write-access to any columnar objects in the row.\n                ")
vacmSecurityToGroupStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 2, 1, 5), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmSecurityToGroupStatus.setDescription("The status of this conceptual row.\n\n                 Until instances of all corresponding columns are\n                 appropriately configured, the value of the\n\n                 corresponding instance of the vacmSecurityToGroupStatus\n                 column is 'notReady'.\n\n                 In particular, a newly created row cannot be made\n                 active until a value has been set for vacmGroupName.\n\n                 The  RowStatus TC [RFC2579] requires that this\n                 DESCRIPTION clause states under which circumstances\n                 other objects in this row can be modified:\n\n                 The value of this object has no effect on whether\n                 other objects in this conceptual row can be modified.\n                ")
vacmAccessTable = MibTable((1, 3, 6, 1, 6, 3, 16, 1, 4), )
if mibBuilder.loadTexts: vacmAccessTable.setDescription("The table of access rights for groups.\n\n                 Each entry is indexed by a groupName, a contextPrefix,\n                 a securityModel and a securityLevel.  To determine\n                 whether access is allowed, one entry from this table\n                 needs to be selected and the proper viewName from that\n                 entry must be used for access control checking.\n\n                 To select the proper entry, follow these steps:\n\n                 1) the set of possible matches is formed by the\n                    intersection of the following sets of entries:\n\n                      the set of entries with identical vacmGroupName\n                      the union of these two sets:\n                       - the set with identical vacmAccessContextPrefix\n                       - the set of entries with vacmAccessContextMatch\n                         value of 'prefix' and matching\n                         vacmAccessContextPrefix\n                      intersected with the union of these two sets:\n                       - the set of entries with identical\n                         vacmSecurityModel\n                       - the set of entries with vacmSecurityModel\n                         value of 'any'\n                      intersected with the set of entries with\n                      vacmAccessSecurityLevel value less than or equal\n                      to the requested securityLevel\n\n                 2) if this set has only one member, we're done\n                    otherwise, it comes down to deciding how to weight\n                    the preferences between ContextPrefixes,\n                    SecurityModels, and SecurityLevels as follows:\n                    a) if the subset of entries with securityModel\n                       matching the securityModel in the message is\n                       not empty, then discard the rest.\n                    b) if the subset of entries with\n                       vacmAccessContextPrefix matching the contextName\n                       in the message is not empty,\n                       then discard the rest\n                    c) discard all entries with ContextPrefixes shorter\n                       than the longest one remaining in the set\n                    d) select the entry with the highest securityLevel\n\n                 Please note that for securityLevel noAuthNoPriv, all\n                 groups are really equivalent since the assumption that\n                 the securityName has been authenticated does not hold.\n                ")
vacmAccessEntry = MibTableRow((1, 3, 6, 1, 6, 3, 16, 1, 4, 1), ).setIndexNames((0, "SNMP-VIEW-BASED-ACM-MIB", "vacmGroupName"), (0, "SNMP-VIEW-BASED-ACM-MIB", "vacmAccessContextPrefix"), (0, "SNMP-VIEW-BASED-ACM-MIB", "vacmAccessSecurityModel"), (0, "SNMP-VIEW-BASED-ACM-MIB", "vacmAccessSecurityLevel"))
if mibBuilder.loadTexts: vacmAccessEntry.setDescription('An access right configured in the Local Configuration\n                 Datastore (LCD) authorizing access to an SNMP context.\n\n                 Entries in this table can use an instance value for\n                 object vacmGroupName even if no entry in table\n                 vacmAccessSecurityToGroupTable has a corresponding\n                 value for object vacmGroupName.\n                ')
vacmAccessContextPrefix = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,32)))
if mibBuilder.loadTexts: vacmAccessContextPrefix.setDescription("In order to gain the access rights allowed by this\n                 conceptual row, a contextName must match exactly\n                 (if the value of vacmAccessContextMatch is 'exact')\n                 or partially (if the value of vacmAccessContextMatch\n                 is 'prefix') to the value of the instance of this\n                 object.\n                ")
vacmAccessSecurityModel = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 2), SnmpSecurityModel())
if mibBuilder.loadTexts: vacmAccessSecurityModel.setDescription('In order to gain the access rights allowed by this\n                 conceptual row, this securityModel must be in use.\n                ')
vacmAccessSecurityLevel = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 3), SnmpSecurityLevel())
if mibBuilder.loadTexts: vacmAccessSecurityLevel.setDescription('The minimum level of security required in order to\n                 gain the access rights allowed by this conceptual\n                 row.  A securityLevel of noAuthNoPriv is less than\n                 authNoPriv which in turn is less than authPriv.\n\n                 If multiple entries are equally indexed except for\n                 this vacmAccessSecurityLevel index, then the entry\n                 which has the highest value for\n                 vacmAccessSecurityLevel is selected.\n                ')
vacmAccessContextMatch = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 4), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2,)).clone(namedValues=NamedValues(("exact", 1), ("prefix", 2),)).clone('exact')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessContextMatch.setDescription('If the value of this object is exact(1), then all\n                 rows where the contextName exactly matches\n                 vacmAccessContextPrefix are selected.\n\n                 If the value of this object is prefix(2), then all\n                 rows where the contextName whose starting octets\n                 exactly match vacmAccessContextPrefix are selected.\n                 This allows for a simple form of wildcarding.\n                ')
vacmAccessReadViewName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 5), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,32)).clone(hexValue="")).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessReadViewName.setDescription('The value of an instance of this object identifies\n                 the MIB view of the SNMP context to which this\n                 conceptual row authorizes read access.\n\n                 The identified MIB view is that one for which the\n                 vacmViewTreeFamilyViewName has the same value as the\n                 instance of this object; if the value is the empty\n                 string or if there is no active MIB view having this\n                 value of vacmViewTreeFamilyViewName, then no access\n                 is granted.\n                ')
vacmAccessWriteViewName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 6), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,32)).clone(hexValue="")).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessWriteViewName.setDescription('The value of an instance of this object identifies\n                 the MIB view of the SNMP context to which this\n                 conceptual row authorizes write access.\n\n                 The identified MIB view is that one for which the\n                 vacmViewTreeFamilyViewName has the same value as the\n                 instance of this object; if the value is the empty\n                 string or if there is no active MIB view having this\n                 value of vacmViewTreeFamilyViewName, then no access\n                 is granted.\n                ')
vacmAccessNotifyViewName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 7), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,32)).clone(hexValue="")).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessNotifyViewName.setDescription('The value of an instance of this object identifies\n                 the MIB view of the SNMP context to which this\n                 conceptual row authorizes access for notifications.\n\n                 The identified MIB view is that one for which the\n                 vacmViewTreeFamilyViewName has the same value as the\n                 instance of this object; if the value is the empty\n                 string or if there is no active MIB view having this\n                 value of vacmViewTreeFamilyViewName, then no access\n                 is granted.\n                ')
vacmAccessStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 8), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessStorageType.setDescription("The storage type for this conceptual row.\n\n                 Conceptual rows having the value 'permanent' need not\n                 allow write-access to any columnar objects in the row.\n                ")
vacmAccessStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 4, 1, 9), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmAccessStatus.setDescription('The status of this conceptual row.\n\n                 The  RowStatus TC [RFC2579] requires that this\n                 DESCRIPTION clause states under which circumstances\n                 other objects in this row can be modified:\n\n                 The value of this object has no effect on whether\n                 other objects in this conceptual row can be modified.\n                ')
vacmMIBViews = MibIdentifier((1, 3, 6, 1, 6, 3, 16, 1, 5))
vacmViewSpinLock = MibScalar((1, 3, 6, 1, 6, 3, 16, 1, 5, 1), TestAndIncr()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: vacmViewSpinLock.setDescription("An advisory lock used to allow cooperating SNMP\n                 Command Generator applications to coordinate their\n                 use of the Set operation in creating or modifying\n                 views.\n\n                 When creating a new view or altering an existing\n                 view, it is important to understand the potential\n                 interactions with other uses of the view.  The\n                 vacmViewSpinLock should be retrieved.  The name of\n                 the view to be created should be determined to be\n                 unique by the SNMP Command Generator application by\n                 consulting the vacmViewTreeFamilyTable.  Finally,\n                 the named view may be created (Set), including the\n                 advisory lock.\n                 If another SNMP Command Generator application has\n                 altered the views in the meantime, then the spin\n                 lock's value will have changed, and so this creation\n                 will fail because it will specify the wrong value for\n                 the spin lock.\n\n                 Since this is an advisory lock, the use of this lock\n                 is not enforced.\n                ")
vacmViewTreeFamilyTable = MibTable((1, 3, 6, 1, 6, 3, 16, 1, 5, 2), )
if mibBuilder.loadTexts: vacmViewTreeFamilyTable.setDescription("Locally held information about families of subtrees\n                 within MIB views.\n\n                 Each MIB view is defined by two sets of view subtrees:\n                   - the included view subtrees, and\n                   - the excluded view subtrees.\n                 Every such view subtree, both the included and the\n\n                 excluded ones, is defined in this table.\n\n                 To determine if a particular object instance is in\n                 a particular MIB view, compare the object instance's\n                 OBJECT IDENTIFIER with each of the MIB view's active\n                 entries in this table.  If none match, then the\n                 object instance is not in the MIB view.  If one or\n                 more match, then the object instance is included in,\n                 or excluded from, the MIB view according to the\n                 value of vacmViewTreeFamilyType in the entry whose\n                 value of vacmViewTreeFamilySubtree has the most\n                 sub-identifiers.  If multiple entries match and have\n                 the same number of sub-identifiers (when wildcarding\n                 is specified with the value of vacmViewTreeFamilyMask),\n                 then the lexicographically greatest instance of\n                 vacmViewTreeFamilyType determines the inclusion or\n                 exclusion.\n\n                 An object instance's OBJECT IDENTIFIER X matches an\n                 active entry in this table when the number of\n                 sub-identifiers in X is at least as many as in the\n                 value of vacmViewTreeFamilySubtree for the entry,\n                 and each sub-identifier in the value of\n                 vacmViewTreeFamilySubtree matches its corresponding\n                 sub-identifier in X.  Two sub-identifiers match\n                 either if the corresponding bit of the value of\n                 vacmViewTreeFamilyMask for the entry is zero (the\n                 'wild card' value), or if they are equal.\n\n                 A 'family' of subtrees is the set of subtrees defined\n                 by a particular combination of values of\n                 vacmViewTreeFamilySubtree and vacmViewTreeFamilyMask.\n\n                 In the case where no 'wild card' is defined in the\n                 vacmViewTreeFamilyMask, the family of subtrees reduces\n                 to a single subtree.\n\n                 When creating or changing MIB views, an SNMP Command\n                 Generator application should utilize the\n                 vacmViewSpinLock to try to avoid collisions.  See\n                 DESCRIPTION clause of vacmViewSpinLock.\n\n                 When creating MIB views, it is strongly advised that\n                 first the 'excluded' vacmViewTreeFamilyEntries are\n                 created and then the 'included' entries.\n\n                 When deleting MIB views, it is strongly advised that\n                 first the 'included' vacmViewTreeFamilyEntries are\n\n                 deleted and then the 'excluded' entries.\n\n                 If a create for an entry for instance-level access\n                 control is received and the implementation does not\n                 support instance-level granularity, then an\n                 inconsistentName error must be returned.\n                ")
vacmViewTreeFamilyEntry = MibTableRow((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1), ).setIndexNames((0, "SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilyViewName"), (0, "SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilySubtree"))
if mibBuilder.loadTexts: vacmViewTreeFamilyEntry.setDescription("Information on a particular family of view subtrees\n                 included in or excluded from a particular SNMP\n                 context's MIB view.\n\n                 Implementations must not restrict the number of\n                 families of view subtrees for a given MIB view,\n                 except as dictated by resource constraints on the\n                 overall number of entries in the\n                 vacmViewTreeFamilyTable.\n\n                 If no conceptual rows exist in this table for a given\n                 MIB view (viewName), that view may be thought of as\n                 consisting of the empty set of view subtrees.\n                ")
vacmViewTreeFamilyViewName = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1,32)))
if mibBuilder.loadTexts: vacmViewTreeFamilyViewName.setDescription('The human readable name for a family of view subtrees.\n                ')
vacmViewTreeFamilySubtree = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 2), ObjectIdentifier())
if mibBuilder.loadTexts: vacmViewTreeFamilySubtree.setDescription('The MIB subtree which when combined with the\n                 corresponding instance of vacmViewTreeFamilyMask\n                 defines a family of view subtrees.\n                ')
vacmViewTreeFamilyMask = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0,16)).clone(hexValue="")).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmViewTreeFamilyMask.setDescription("The bit mask which, in combination with the\n                 corresponding instance of vacmViewTreeFamilySubtree,\n                 defines a family of view subtrees.\n\n                 Each bit of this bit mask corresponds to a\n                 sub-identifier of vacmViewTreeFamilySubtree, with the\n                 most significant bit of the i-th octet of this octet\n                 string value (extended if necessary, see below)\n                 corresponding to the (8*i - 7)-th sub-identifier, and\n                 the least significant bit of the i-th octet of this\n                 octet string corresponding to the (8*i)-th\n                 sub-identifier, where i is in the range 1 through 16.\n\n                 Each bit of this bit mask specifies whether or not\n                 the corresponding sub-identifiers must match when\n                 determining if an OBJECT IDENTIFIER is in this\n                 family of view subtrees; a '1' indicates that an\n                 exact match must occur; a '0' indicates 'wild card',\n                 i.e., any sub-identifier value matches.\n\n                 Thus, the OBJECT IDENTIFIER X of an object instance\n                 is contained in a family of view subtrees if, for\n                 each sub-identifier of the value of\n                 vacmViewTreeFamilySubtree, either:\n\n                   the i-th bit of vacmViewTreeFamilyMask is 0, or\n\n                   the i-th sub-identifier of X is equal to the i-th\n                   sub-identifier of the value of\n                   vacmViewTreeFamilySubtree.\n\n                 If the value of this bit mask is M bits long and\n\n                 there are more than M sub-identifiers in the\n                 corresponding instance of vacmViewTreeFamilySubtree,\n                 then the bit mask is extended with 1's to be the\n                 required length.\n\n                 Note that when the value of this object is the\n                 zero-length string, this extension rule results in\n                 a mask of all-1's being used (i.e., no 'wild card'),\n                 and the family of view subtrees is the one view\n                 subtree uniquely identified by the corresponding\n                 instance of vacmViewTreeFamilySubtree.\n\n                 Note that masks of length greater than zero length\n                 do not need to be supported.  In this case this\n                 object is made read-only.\n                ")
vacmViewTreeFamilyType = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 4), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2,)).clone(namedValues=NamedValues(("included", 1), ("excluded", 2),)).clone('included')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmViewTreeFamilyType.setDescription('Indicates whether the corresponding instances of\n                 vacmViewTreeFamilySubtree and vacmViewTreeFamilyMask\n                 define a family of view subtrees which is included in\n                 or excluded from the MIB view.\n                ')
vacmViewTreeFamilyStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmViewTreeFamilyStorageType.setDescription("The storage type for this conceptual row.\n\n                 Conceptual rows having the value 'permanent' need not\n                 allow write-access to any columnar objects in the row.\n                ")
vacmViewTreeFamilyStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 16, 1, 5, 2, 1, 6), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: vacmViewTreeFamilyStatus.setDescription('The status of this conceptual row.\n\n                 The  RowStatus TC [RFC2579] requires that this\n                 DESCRIPTION clause states under which circumstances\n                 other objects in this row can be modified:\n\n                 The value of this object has no effect on whether\n                 other objects in this conceptual row can be modified.\n                ')
vacmMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 16, 2, 1))
vacmMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 16, 2, 2))
vacmMIBCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 16, 2, 1, 1)).setObjects(*(("SNMP-VIEW-BASED-ACM-MIB", "vacmBasicGroup"),))
if mibBuilder.loadTexts: vacmMIBCompliance.setDescription('The compliance statement for SNMP engines which\n                 implement the SNMP View-based Access Control Model\n                 configuration MIB.\n                ')
vacmBasicGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 16, 2, 2, 1)).setObjects(*(("SNMP-VIEW-BASED-ACM-MIB", "vacmContextName"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmGroupName"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmSecurityToGroupStorageType"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmSecurityToGroupStatus"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessContextMatch"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessReadViewName"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessWriteViewName"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessNotifyViewName"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessStorageType"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmAccessStatus"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmViewSpinLock"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilyMask"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilyType"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilyStorageType"), ("SNMP-VIEW-BASED-ACM-MIB", "vacmViewTreeFamilyStatus"),))
if mibBuilder.loadTexts: vacmBasicGroup.setDescription('A collection of objects providing for remote\n                 configuration of an SNMP engine which implements\n\n                 the SNMP View-based Access Control Model.\n                ')
mibBuilder.exportSymbols("SNMP-VIEW-BASED-ACM-MIB", vacmMIBObjects=vacmMIBObjects, vacmSecurityName=vacmSecurityName, vacmViewTreeFamilyMask=vacmViewTreeFamilyMask, vacmSecurityToGroupStorageType=vacmSecurityToGroupStorageType, vacmAccessContextMatch=vacmAccessContextMatch, vacmContextEntry=vacmContextEntry, vacmSecurityModel=vacmSecurityModel, vacmAccessReadViewName=vacmAccessReadViewName, snmpVacmMIB=snmpVacmMIB, vacmViewTreeFamilyEntry=vacmViewTreeFamilyEntry, vacmSecurityToGroupStatus=vacmSecurityToGroupStatus, vacmMIBCompliances=vacmMIBCompliances, vacmContextName=vacmContextName, vacmAccessTable=vacmAccessTable, vacmViewTreeFamilyTable=vacmViewTreeFamilyTable, vacmSecurityToGroupEntry=vacmSecurityToGroupEntry, vacmContextTable=vacmContextTable, vacmMIBGroups=vacmMIBGroups, vacmViewSpinLock=vacmViewSpinLock, vacmViewTreeFamilySubtree=vacmViewTreeFamilySubtree, vacmMIBCompliance=vacmMIBCompliance, vacmGroupName=vacmGroupName, vacmAccessWriteViewName=vacmAccessWriteViewName, vacmBasicGroup=vacmBasicGroup, vacmAccessStorageType=vacmAccessStorageType, vacmSecurityToGroupTable=vacmSecurityToGroupTable, vacmAccessContextPrefix=vacmAccessContextPrefix, vacmAccessSecurityModel=vacmAccessSecurityModel, vacmAccessEntry=vacmAccessEntry, vacmAccessSecurityLevel=vacmAccessSecurityLevel, vacmAccessNotifyViewName=vacmAccessNotifyViewName, PYSNMP_MODULE_ID=snmpVacmMIB, vacmMIBViews=vacmMIBViews, vacmViewTreeFamilyStorageType=vacmViewTreeFamilyStorageType, vacmAccessStatus=vacmAccessStatus, vacmViewTreeFamilyType=vacmViewTreeFamilyType, vacmViewTreeFamilyViewName=vacmViewTreeFamilyViewName, vacmMIBConformance=vacmMIBConformance, vacmViewTreeFamilyStatus=vacmViewTreeFamilyStatus)
