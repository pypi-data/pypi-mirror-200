from typing import Literal

_ObjectType = Literal [
    "AccessPointGroup",
    "Action",
    "ActivationSpec",
    "ActivationSpecTemplateProps",
    "ActiveAffinityType",
    "ActivitySessionService",
    "AdminAgentRegistration",
    "AdminObject",
    "AdminObjectTemplateProps",
    "AdminServerAuthentication",
    "AdminService",
    "AdministeredObjectResource",
    "AffinityType",
    "AgeCondition",
    "Agent",
    "AllActivePolicy",
    "AllAuthenticatedUsersExt",
    "AllAuthenticatedUsersInTrustedRealmsExt",
    "AppAudit",
    "AppPlacementController",
    "AppSecurity",
    "Application",
    "ApplicationClientFile",
    "ApplicationConfig",
    "ApplicationContainer",
    "ApplicationDeployment",
    "ApplicationManagementService",
    "ApplicationProfileService",
    "ApplicationResources",
    "ApplicationServer",
    "ApplicationServerClusterMapping",
    "ApplicationServerClusterMember",
    "ApplicationServerEndpoint",
    "ApplicationServerMapping",
    "ApplicationServerRoute",
    "ApplicationServerTimeMapping",
    "Archive",
    "Audit",
    "AuditCommon",
    "AuditEventFactory",
    "AuditNotificationMonitor",
    "AuditPolicy",
    "AuditServiceProvider",
    "AuditSpecification",
    "AuthConfigProvider",
    "AuthConfigProviderEntry",
    "AuthMechanism",
    "AuthModule",
    "AuthenticationMechanism",
    "AuthenticationTarget",
    "AuthorizationConfig",
    "AuthorizationGroup",
    "AuthorizationGroupMember",
    "AuthorizationProvider",
    "AuthorizationTableExt",
    "AuthorizationTableImpl",
    "AutonomicRequestFlowManager",
    "AverageResponseTimeGoal",
    "BackupCluster",
    "BridgeInterface",
    "CACertificate",
    "CAClient",
    "CMPConnectorFactory",
    "CORBAObjectNameSpaceBinding",
    "CacheInstance",
    "CacheInstanceService",
    "CacheProvider",
    "CachingAction",
    "Cell",
    "CellManager",
    "CellRoute",
    "Certificate",
    "Chain",
    "Checkpoint",
    "CheckpointDocument",
    "Classloader",
    "ClientModuleDeployment",
    "ClientModuleRef",
    "ClusterAddressEndPoint",
    "ClusterAddressProperties",
    "ClusterAdvisor",
    "ClusterMember",
    "ClusteredTarget",
    "CommonSecureInterop",
    "CompatibilityDescriptionGroup",
    "CompensationService",
    "CompletionTimeGoal",
    "Component",
    "CompressionAction",
    "ConfigProperty",
    "ConfigSynchronizationService",
    "ConnectionDefTemplateProps",
    "ConnectionDefinition",
    "ConnectionFactory",
    "ConnectionFactoryResource",
    "ConnectionPool",
    "ConnectionTest",
    "Connector",
    "ConnectorCluster",
    "ConnectorModuleDeployment",
    "ConnectorModuleRef",
    "Container",
    "ContentMapping",
    "Contributor",
    "Cookie",
    "CookieMapping",
    "CoreGroup",
    "CoreGroupAccessPoint",
    "CoreGroupBridgeService",
    "CoreGroupBridgeSettings",
    "CoreGroupServer",
    "CryptoHardwareToken",
    "CustomAdvisor",
    "CustomAdvisorMapping",
    "CustomAdvisorPolicy",
    "CustomAuthMechanism",
    "CustomConditionTemplate",
    "CustomConditionTemplates",
    "CustomElasticityAction",
    "CustomErrorPagePolicy",
    "CustomHealthAction",
    "CustomProcessDefs",
    "CustomService",
    "CustomUserRegistry",
    "DCSInboundChannel",
    "DPClonableDeviceSettings",
    "DPClonableDeviceSettingsVersion",
    "DPDeployableConfiguration",
    "DPDevice",
    "DPDomain",
    "DPDomainVersion",
    "DPFirmware",
    "DPFirmwareVersion",
    "DPManagedSet",
    "DPManager",
    "DPVersion",
    "DRSConnectionPool",
    "DRSPartition",
    "DRSSerialization",
    "DRSSettings",
    "DataPowerMgrInboundChannel",
    "DataReplication",
    "DataReplicationDomain",
    "DataSource",
    "DataSourceDefinition",
    "DebugService",
    "DefaultSIPApplicationRouter",
    "DeployedMiddlewareApp",
    "DeployedMiddlewareAppEdition",
    "DeployedObject",
    "DeployedObjectConfig",
    "DeployedObjectProxyConfig",
    "Deployment",
    "DeploymentTarget",
    "DeploymentTargetMapping",
    "Description",
    "DescriptionGroup",
    "DescriptiveProperty",
    "DescriptivePropertyGroup",
    "DiagnosticProviderService",
    "DigestAuthentication",
    "DiscoverableDescriptiveProperty",
    "DiscretionaryGoal",
    "DiskCacheCustomPerformanceSettings",
    "DiskCacheEvictionPolicy",
    "DisplayDescriptor",
    "DisplayName",
    "DynamicCache",
    "DynamicCluster",
    "DynamicReload",
    "DynamicSSLConfigSelection",
    "DynamicWtCtrlr",
    "EARFile",
    "EJBAsync",
    "EJBCache",
    "EJBContainer",
    "EJBDeployment",
    "EJBJarFile",
    "EJBLocalRef",
    "EJBModuleConfiguration",
    "EJBModuleDeployment",
    "EJBModuleRef",
    "EJBTimer",
    "EjbNameSpaceBinding",
    "EjbRef",
    "ElasticityAction",
    "ElasticityClass",
    "ElasticityCustomProcessDefs",
    "ElasticityType",
    "EmailNotifications",
    "EndPoint",
    "EndPointRef",
    "EnterpriseBeanConfig",
    "EnvEntry",
    "ErrorMapping",
    "EveryoneExt",
    "ExecutionTimeAndThreadLimit",
    "ExtendedApplicationData",
    "ExtendedRepositoryService",
    "Extension",
    "ExtensionMBean",
    "ExtensionMBeanProvider",
    "ExternalCacheGroup",
    "ExternalCacheGroupMember",
    "ExternalDomain",
    "ExternalFile",
    "ExternalFileService",
    "ExternallyManagedHTTPServer",
    "FRCACacheGroupMember",
    "FailRoute",
    "File",
    "FileTransferService",
    "Filter",
    "ForeignCell",
    "ForeignServer",
    "GCPercentageCondition",
    "GSCMember",
    "GSCMemberEndpoint",
    "GenericChannelData",
    "GenericChannelFactory",
    "GenericClusterRoute",
    "GenericInboundChannel",
    "GenericJMSConnectionFactory",
    "GenericJMSDestination",
    "GenericOutboundChannel",
    "GenericServerCluster",
    "GenericServerClusterMapping",
    "GenericServerClusterRoute",
    "GenericServerClusterTimeMapping",
    "GenericServerEndpoint",
    "GridClassRules",
    "GridMatchRule",
    "GridScheduler",
    "GridWorkGoal",
    "GroupExt",
    "HAManagerPolicy",
    "HAManagerService",
    "HPELLog",
    "HPELTextLog",
    "HPELTrace",
    "HTTPAccessLoggingService",
    "HTTPConnector",
    "HTTPInboundChannel",
    "HTTPInboundChannelLogging",
    "HTTPOutboundChannel",
    "HTTPProxyServerSettings",
    "HTTPQueueInboundChannel",
    "HTTPRequestCompressionAction",
    "HTTPRequestHeaderAction",
    "HTTPResponseCompressionAction",
    "HTTPResponseHeaderAction",
    "HTTPTransport",
    "HTTPTunnelInboundChannel",
    "HTTPTunnelOutboundChannel",
    "HeaderAction",
    "HeaderCondition",
    "HealthAction",
    "HealthClass",
    "HealthCondition",
    "HealthController",
    "HealthTime",
    "HighPerformanceExtensibleLogging",
    "HostAlias",
    "I18NService",
    "IIOPLayer",
    "IIOPSecurityProtocol",
    "IIOPTransport",
    "IPCConnector",
    "IPSprayer",
    "IconType",
    "Identity",
    "IdentityAssertionLayer",
    "IdentityAssertionQOP",
    "IdentityAssertionTypeAssociation",
    "InboundResourceAdapter",
    "InboundTransportChannel",
    "IndirectLookupNameSpaceBinding",
    "InjectionTarget",
    "InstancePool",
    "IntelligentManagement",
    "Interceptor",
    "InvalidationSchedule",
    "J2CActivationSpec",
    "J2CAdminObject",
    "J2CConnectionFactory",
    "J2CResourceAdapter",
    "J2EEEAttribute",
    "J2EEEObject",
    "J2EEResourceFactory",
    "J2EEResourceProperty",
    "J2EEResourcePropertySet",
    "J2EEResourceProvider",
    "JAASAuthData",
    "JAASConfiguration",
    "JAASConfigurationEntry",
    "JAASLoginModule",
    "JASPIConfiguration",
    "JAXRPCHandler",
    "JAXRPCHandlerList",
    "JAXRPCHeader",
    "JAXWSHandler",
    "JAXWSHandlerList",
    "JDBCProvider",
    "JFAPFactory",
    "JFAPInboundChannel",
    "JFAPOutboundChannel",
    "JMSConnectionFactory",
    "JMSConnectionFactoryResource",
    "JMSConnector",
    "JMSDestination",
    "JMSDestinationResource",
    "JMSProvider",
    "JMSServer",
    "JMSTransport",
    "JMXConnector",
    "JNDIEnvRefsGroup",
    "JSR160RMIConnector",
    "JavaEEDefaultResources",
    "JavaPersistenceAPIService",
    "JavaProcessDef",
    "JavaVirtualMachine",
    "JavaVirtualMachinePreset",
    "JobClass",
    "JobLogLimit",
    "JobManager",
    "JobManagerRegistration",
    "KRB5",
    "Key",
    "KeyManager",
    "KeyReference",
    "KeySet",
    "KeySetGroup",
    "KeyStore",
    "KeyStoreFile",
    "LDAPSearchFilter",
    "LDAPUserRegistry",
    "LSDConnection",
    "LTPA",
    "Library",
    "LibraryRef",
    "License",
    "LifecycleCallbackType",
    "Listener",
    "ListenerPort",
    "Liveness",
    "LocalErrorPagePolicy",
    "LocalOSUserRegistry",
    "LocalRoute",
    "LogFile",
    "LooseApplication",
    "LooseArchive",
    "LooseArchiveMetadata",
    "LooseConfiguration",
    "LooseLibrary",
    "LooseModule",
    "LooseWARFile",
    "MOfNPolicy",
    "MQConnectionFactory",
    "MQFAPInboundChannel",
    "MQFAPOutboundChannel",
    "MQQueue",
    "MQQueueConnectionFactory",
    "MQTopic",
    "MQTopicConnectionFactory",
    "MailProvider",
    "MailSession",
    "MailSessionResource",
    "ManagedMiddlewareAppEdition",
    "ManagedNode",
    "ManagedObject",
    "ManagementScope",
    "MappingModule",
    "MatchCriteria",
    "MatchRule",
    "MemoryCacheEvictionPolicy",
    "MemoryCondition",
    "MemoryLeakAlgorithm",
    "MessageAdapter",
    "MessageCondition",
    "MessageDestination",
    "MessageDestinationRef",
    "MessageLayer",
    "MessageListener",
    "MessageListenerService",
    "MessageQOP",
    "MethodMessageCondition",
    "MiddlewareApp",
    "MiddlewareAppEdition",
    "MiddlewareAppScript",
    "MiddlewareClusterTarget",
    "MiddlewareDescriptor",
    "MiddlewareModule",
    "MiddlewareServerTarget",
    "MiddlewareTarget",
    "MiddlewareVersionDescriptor",
    "MiddlewareWebModule",
    "MimeEntry",
    "ModuleConfig",
    "ModuleDeployment",
    "ModuleFile",
    "ModuleRef",
    "ModuleShare",
    "MonitoredDirectoryDeployment",
    "MonitoringPolicy",
    "MultiBrokerRoutingEntry",
    "MultiCellOverlayBridge",
    "MultibrokerDomain",
    "NameBinding",
    "NameServer",
    "NameSpaceBinding",
    "NamedEndPoint",
    "NamedJavaProcessDef",
    "NamedProcessDef",
    "NamingContext",
    "NewClass",
    "NoOpPolicy",
    "Node",
    "NodeAgent",
    "NodeGroup",
    "NodeGroupMember",
    "OLTPWorkGoal",
    "ORBInboundChannel",
    "ORBPlugin",
    "ObjectCacheInstance",
    "ObjectPool",
    "ObjectPoolManagerInfo",
    "ObjectPoolProvider",
    "ObjectPoolService",
    "ObjectRequestBroker",
    "OnDemandRouter",
    "OneOfNPolicy",
    "OutboundResourceAdapter",
    "OutboundTransportChannel",
    "OutputQueueLimit",
    "OutputRedirect",
    "OverlayEndpoint",
    "PME502ServerExtension",
    "PME51ServerExtension",
    "PMEClusterExtension",
    "PMEServerExtension",
    "PMIModule",
    "PMIRMFilter",
    "PMIRMFilterValue",
    "PMIRequestMetrics",
    "PMIService",
    "ParamValue",
    "PassiveAffinityType",
    "PeerAccessPoint",
    "PeerCoreGroup",
    "PercentileResponseTimeGoal",
    "PerformanceGoal",
    "PersistenceContextRef",
    "PersistenceUnitRef",
    "PluginConfigPolicy",
    "PluginConfigService",
    "PluginProperties",
    "PluginServerClusterProperties",
    "Policy",
    "PortletContainer",
    "PreferenceSet",
    "Preferences",
    "PreferredServerPolicy",
    "PrimaryAdminExt",
    "ProcessDef",
    "ProcessExecution",
    "Property",
    "PropertySet",
    "ProtocolProvider",
    "Proxy",
    "ProxyAction",
    "ProxyInboundChannel",
    "ProxyOverrides",
    "ProxyRuleExpression",
    "ProxyServer",
    "ProxySettings",
    "ProxyVirtualHost",
    "ProxyVirtualHostConfig",
    "ProxyVirtualHostSettings",
    "QName",
    "QualityOfProtection",
    "QueueTimeGoal",
    "RARFile",
    "RASLoggingService",
    "RMIConnector",
    "RMQChannelFactory",
    "RMQOutboundChannel",
    "RSAToken",
    "ReadOnlyDirectory",
    "RecoveryLog",
    "RedirectRoute",
    "Referenceable",
    "RemoteCellAccessPoint",
    "RemoteCellOverrides",
    "RepositoryService",
    "RequiredConfigPropertyType",
    "ResourceAdapter",
    "ResourceEnvEntry",
    "ResourceEnvRef",
    "ResourceEnvironmentProvider",
    "ResourceRef",
    "ResponseCondition",
    "RestartTime",
    "RewritingAction",
    "RewritingPolicy",
    "RewritingRule",
    "RoleAssignmentExt",
    "RoleBasedAuthorization",
    "Route",
    "RoutingAction",
    "RoutingPolicy",
    "RoutingRule",
    "Rule",
    "Rules",
    "Ruleset",
    "RunAsSpecifiedIdentity",
    "SARClusterTarget",
    "SARDeploymentTarget",
    "SARServerTarget",
    "SIBAbstractDestination",
    "SIBAudit",
    "SIBAuthAlias",
    "SIBAuthBrowser",
    "SIBAuthBusConnect",
    "SIBAuthCreator",
    "SIBAuthDefault",
    "SIBAuthForeignBus",
    "SIBAuthForeignDestination",
    "SIBAuthGroup",
    "SIBAuthIdentityAdopter",
    "SIBAuthPort",
    "SIBAuthQueue",
    "SIBAuthReceiver",
    "SIBAuthSender",
    "SIBAuthSpace",
    "SIBAuthTopic",
    "SIBAuthTopicSpace",
    "SIBAuthTopicSpaceBase",
    "SIBAuthTopicSpaceRoot",
    "SIBAuthUser",
    "SIBAuthWebService",
    "SIBBootstrapMember",
    "SIBContextInfo",
    "SIBDatastore",
    "SIBDestination",
    "SIBDestinationAlias",
    "SIBDestinationDefault",
    "SIBDestinationForeign",
    "SIBDestinationMediation",
    "SIBDestinationMediationRef",
    "SIBFilestore",
    "SIBForeignBus",
    "SIBGatewayLink",
    "SIBJMSConnectionFactory",
    "SIBJMSProvider",
    "SIBJMSQueue",
    "SIBJMSQueueConnectionFactory",
    "SIBJMSTopic",
    "SIBJMSTopicConnectionFactory",
    "SIBLinkRef",
    "SIBLocalizationPoint",
    "SIBLocalizationPointRef",
    "SIBMQClientLink",
    "SIBMQClientLinkAdvancedProperties",
    "SIBMQLink",
    "SIBMQLinkReceiverChannel",
    "SIBMQLinkSenderChannel",
    "SIBMQLinkSenderChannelLocalizationPoint",
    "SIBMQLocalizationPointProxy",
    "SIBMQMediationPointProxy",
    "SIBMQQueueLocalizationPointProxy",
    "SIBMQServer",
    "SIBMQServerBusMember",
    "SIBMediation",
    "SIBMediationExecutionPoint",
    "SIBMediationInstance",
    "SIBMediationLocalizationPoint",
    "SIBMessagingEngine",
    "SIBPSBBrokerProfile",
    "SIBPSBBrokerTransactionality",
    "SIBPSBTopicMapping",
    "SIBPSBTopicTransactionality",
    "SIBPermittedChain",
    "SIBPort",
    "SIBQualifiedDestinationName",
    "SIBQueue",
    "SIBQueueLocalizationPoint",
    "SIBService",
    "SIBTopicSpace",
    "SIBTopicSpaceAudit",
    "SIBTopicSpaceLocalizationPoint",
    "SIBTopicSpaceMapEntry",
    "SIBTopicSpaceMapping",
    "SIBVirtualGatewayLink",
    "SIBVirtualLink",
    "SIBVirtualMQLink",
    "SIBWMQServerEndpoint",
    "SIBWMQServerSvrconnChannel",
    "SIBWSBusConnectionProperty",
    "SIBWSEndpointListener",
    "SIBWSEndpointListenerReference",
    "SIBWSInboundPort",
    "SIBWSInboundPortReference",
    "SIBWSInboundService",
    "SIBWSOutboundPort",
    "SIBWSOutboundService",
    "SIBWSSecurityInboundConfig",
    "SIBWSSecurityOutboundConfig",
    "SIBWSSecurityRequestConsumerBindingConfig",
    "SIBWSSecurityRequestGeneratorBindingConfig",
    "SIBWSSecurityRequestReceiverBindingConfig",
    "SIBWSSecurityRequestSenderBindingConfig",
    "SIBWSSecurityResponseConsumerBindingConfig",
    "SIBWSSecurityResponseGeneratorBindingConfig",
    "SIBWSSecurityResponseReceiverBindingConfig",
    "SIBWSSecurityResponseSenderBindingConfig",
    "SIBWSUDDIPublication",
    "SIBWSWSDLLocation",
    "SIBWebService",
    "SIBus",
    "SIBusMember",
    "SIBusMemberTarget",
    "SIPApplicationRouter",
    "SIPApplicationRouters",
    "SIPContainer",
    "SIPContainerInboundChannel",
    "SIPInboundChannel",
    "SIPMessageCondition",
    "SIPOutboundChannel",
    "SIPProxyInboundChannel",
    "SIPProxyServerSettings",
    "SIPProxySettings",
    "SIPRoutingRule",
    "SOAPConnector",
    "SPNEGO",
    "SSLConfig",
    "SSLConfigGroup",
    "SSLInboundChannel",
    "SSLOutboundChannel",
    "SWAMAuthentication",
    "SchedulerConfiguration",
    "SchedulerProvider",
    "SchedulerService",
    "SecureAssociationService",
    "SecureClusterAddressEndPoint",
    "SecureSessionCookie",
    "SecureSocketLayer",
    "Security",
    "SecurityCommon",
    "SecurityDomain",
    "SecurityDomainMember",
    "SecurityIdentity",
    "SecurityPermission",
    "SecurityProtocolConfig",
    "SecurityProtocolQOP",
    "SecurityRole",
    "SecurityRoleExt",
    "SecurityRoleRef",
    "SecurityServer",
    "Server",
    "ServerCluster",
    "ServerComponent",
    "ServerEntry",
    "ServerExt",
    "ServerIdentity",
    "ServerIndex",
    "ServerInstance",
    "ServerTarget",
    "Service",
    "ServiceClass",
    "ServiceClassGoal",
    "ServiceContext",
    "ServiceLog",
    "ServletCacheInstance",
    "SessionBeanConfig",
    "SessionDatabasePersistence",
    "SessionManager",
    "SessionSecurity",
    "SingleSignon",
    "SpecialSubjectExt",
    "Stack",
    "StandAloneApplicationServerMapping",
    "StartupBeansService",
    "StateManageable",
    "StatefulSessionBeanConfig",
    "StaticCachePolicy",
    "StaticCacheRule",
    "StaticFileServingPolicy",
    "StaticPolicy",
    "StatisticsProvider",
    "StormDrainCondition",
    "StreamRedirect",
    "StringNameSpaceBinding",
    "StuckRequestCondition",
    "SubjectExt",
    "SystemMessageServer",
    "TAInterceptor",
    "TCPFactory",
    "TCPInboundChannel",
    "TCPOutboundChannel",
    "TPVService",
    "TargetMembership",
    "TaskProvider",
    "ThreadPool",
    "ThreadPoolManager",
    "TimeMapping",
    "TimerManagerInfo",
    "TimerManagerProvider",
    "Timers",
    "TivoliPerfViewer",
    "TraceLog",
    "TraceService",
    "TraceSpecification",
    "TransactionClass",
    "TransactionClassModule",
    "TransactionService",
    "Transport",
    "TransportChannel",
    "TransportChannelFactory",
    "TransportChannelService",
    "TransportLayer",
    "TransportQOP",
    "TrustAssociation",
    "TrustManager",
    "TrustedAuthenticationRealm",
    "TuningParams",
    "TunnelAccessPointGroup",
    "TunnelPeerAccessPoint",
    "TunnelTemplate",
    "TypedProperty",
    "UDDIConfig",
    "UDDIReference",
    "UDPInboundChannel",
    "UDPOutboundChannel",
    "URIGroup",
    "URL",
    "URLProvider",
    "UnmanagedMiddlewareAppEdition",
    "UseCallerIdentity",
    "UserDefinedLine",
    "UserExt",
    "UserRegistry",
    "VariableMap",
    "VariableSubstitutionEntry",
    "VirtualHost",
    "VisualizationDataLog",
    "VisualizationDataService",
    "WARFile",
    "WARFragmentFile",
    "WAS40ConnectionPool",
    "WAS40DataSource",
    "WASAbstractAuthData",
    "WASAddressingType",
    "WASAdministeredObjectResource",
    "WASBasicAuthData",
    "WASConnectionFactoryResource",
    "WASDataSourceDefinition",
    "WASDataSourceDefinitionBinding",
    "WASEjbRef",
    "WASEjbRefBinding",
    "WASEnvEntry",
    "WASHandler",
    "WASHandlerChain",
    "WASHandlerChains",
    "WASJMSConnectionFactoryResource",
    "WASJMSDestinationResource",
    "WASMailSessionResource",
    "WASMessageDestinationRef",
    "WASMessageDestinationRefBinding",
    "WASParamValue",
    "WASPersistenceContextRef",
    "WASPersistenceUnitRef",
    "WASPortComponentRef",
    "WASQName",
    "WASQueue",
    "WASQueueConnectionFactory",
    "WASResourceEnvRef",
    "WASResourceEnvRefBinding",
    "WASResourceRef",
    "WASResourceRefBinding",
    "WASResourceRefExtension",
    "WASRespectBindingType",
    "WASServiceRef",
    "WASTopic",
    "WASTopicConnectionFactory",
    "WIMUserRegistry",
    "WLMCoreGroupBridgePlugin",
    "WSByteBufferService",
    "WSCertificateExpirationMonitor",
    "WSGWGatewayService",
    "WSGWInstance",
    "WSGWProxyService",
    "WSGWTargetService",
    "WSNAdministeredSubscriber",
    "WSNInstanceDocument",
    "WSNService",
    "WSNServicePoint",
    "WSNTopicNamespace",
    "WSNotification",
    "WSPassword",
    "WSPasswordEncryption",
    "WSPasswordLocator",
    "WSSchedule",
    "WSSecurityScannerMonitor",
    "WebContainer",
    "WebContainerInboundChannel",
    "WebModuleConfig",
    "WebModuleDeployment",
    "WebModuleRef",
    "WebServer",
    "WebserverPluginSettings",
    "WeightAdvisor",
    "WorkAreaPartition",
    "WorkAreaPartitionService",
    "WorkAreaService",
    "WorkClass",
    "WorkClassModule",
    "WorkManagerInfo",
    "WorkManagerProvider",
    "WorkManagerService",
    "WorkloadCondition",
    "WorkloadManagementPolicy",
    "WorkloadManagementServer",
    "com.ibm.etools.webservice.wsbnd.DefaultEndpointURIPrefix",
    "com.ibm.etools.webservice.wsbnd.PCBinding",
    "com.ibm.etools.webservice.wsbnd.RouterModule",
    "com.ibm.etools.webservice.wsbnd.SecurityRequestConsumerBindingConfig",
    "com.ibm.etools.webservice.wsbnd.SecurityRequestReceiverBindingConfig",
    "com.ibm.etools.webservice.wsbnd.SecurityResponseGeneratorBindingConfig",
    "com.ibm.etools.webservice.wsbnd.SecurityResponseSenderBindingConfig",
    "com.ibm.etools.webservice.wsbnd.WSBinding",
    "com.ibm.etools.webservice.wsbnd.WSDescBinding",
    "com.ibm.etools.webservice.wscbnd.BasicAuth",
    "com.ibm.etools.webservice.wscbnd.ClientBinding",
    "com.ibm.etools.webservice.wscbnd.ComponentScopedRefs",
    "com.ibm.etools.webservice.wscbnd.DefaultMapping",
    "com.ibm.etools.webservice.wscbnd.LoginBinding",
    "com.ibm.etools.webservice.wscbnd.PortQnameBinding",
    "com.ibm.etools.webservice.wscbnd.SecurityRequestGeneratorBindingConfig",
    "com.ibm.etools.webservice.wscbnd.SecurityRequestSenderBindingConfig",
    "com.ibm.etools.webservice.wscbnd.SecurityResponseConsumerBindingConfig",
    "com.ibm.etools.webservice.wscbnd.SecurityResponseReceiverBindingConfig",
    "com.ibm.etools.webservice.wscbnd.ServiceRef",
    "com.ibm.etools.webservice.wscext.ClientServiceConfig",
    "com.ibm.etools.webservice.wscext.ComponentScopedRefs",
    "com.ibm.etools.webservice.wscext.DefaultMapping",
    "com.ibm.etools.webservice.wscext.LoginConfig",
    "com.ibm.etools.webservice.wscext.PortQnameBinding",
    "com.ibm.etools.webservice.wscext.SecurityRequestGeneratorServiceConfig",
    "com.ibm.etools.webservice.wscext.SecurityRequestSenderServiceConfig",
    "com.ibm.etools.webservice.wscext.SecurityResponseConsumerServiceConfig",
    "com.ibm.etools.webservice.wscext.SecurityResponseReceiverServiceConfig",
    "com.ibm.etools.webservice.wscext.ServiceRef",
    "com.ibm.etools.webservice.wscext.WsClientExtension",
    "com.ibm.etools.webservice.wscommonbnd.AlgorithmMapping",
    "com.ibm.etools.webservice.wscommonbnd.AlgorithmURI",
    "com.ibm.etools.webservice.wscommonbnd.CRL",
    "com.ibm.etools.webservice.wscommonbnd.CallbackHandler",
    "com.ibm.etools.webservice.wscommonbnd.CallbackHandlerFactory",
    "com.ibm.etools.webservice.wscommonbnd.CanonicalizationMethod",
    "com.ibm.etools.webservice.wscommonbnd.CertPathSettings",
    "com.ibm.etools.webservice.wscommonbnd.CertStoreList",
    "com.ibm.etools.webservice.wscommonbnd.CertStoreRef",
    "com.ibm.etools.webservice.wscommonbnd.CollectionCertStore",
    "com.ibm.etools.webservice.wscommonbnd.Consumerbindingref",
    "com.ibm.etools.webservice.wscommonbnd.DataEncryptionMethod",
    "com.ibm.etools.webservice.wscommonbnd.DigestMethod",
    "com.ibm.etools.webservice.wscommonbnd.EncryptionInfo",
    "com.ibm.etools.webservice.wscommonbnd.EncryptionKey",
    "com.ibm.etools.webservice.wscommonbnd.EncryptionKeyInfo",
    "com.ibm.etools.webservice.wscommonbnd.Generatorbindingref",
    "com.ibm.etools.webservice.wscommonbnd.JAASConfig",
    "com.ibm.etools.webservice.wscommonbnd.KeyEncryptionMethod",
    "com.ibm.etools.webservice.wscommonbnd.KeyInfo",
    "com.ibm.etools.webservice.wscommonbnd.KeyInfoSignature",
    "com.ibm.etools.webservice.wscommonbnd.KeyLocator",
    "com.ibm.etools.webservice.wscommonbnd.KeyLocatorMapping",
    "com.ibm.etools.webservice.wscommonbnd.KeyStore",
    "com.ibm.etools.webservice.wscommonbnd.LDAPCertStore",
    "com.ibm.etools.webservice.wscommonbnd.LDAPServer",
    "com.ibm.etools.webservice.wscommonbnd.LoginMapping",
    "com.ibm.etools.webservice.wscommonbnd.NonceCaching",
    "com.ibm.etools.webservice.wscommonbnd.Parameter",
    "com.ibm.etools.webservice.wscommonbnd.PartReference",
    "com.ibm.etools.webservice.wscommonbnd.SignatureMethod",
    "com.ibm.etools.webservice.wscommonbnd.SigningInfo",
    "com.ibm.etools.webservice.wscommonbnd.SigningKey",
    "com.ibm.etools.webservice.wscommonbnd.SigningKeyInfo",
    "com.ibm.etools.webservice.wscommonbnd.TokenConsumer",
    "com.ibm.etools.webservice.wscommonbnd.TokenGenerator",
    "com.ibm.etools.webservice.wscommonbnd.TokenReference",
    "com.ibm.etools.webservice.wscommonbnd.TokenValueType",
    "com.ibm.etools.webservice.wscommonbnd.Transform",
    "com.ibm.etools.webservice.wscommonbnd.TrustAnchor",
    "com.ibm.etools.webservice.wscommonbnd.TrustAnchorRef",
    "com.ibm.etools.webservice.wscommonbnd.TrustAnyCertificate",
    "com.ibm.etools.webservice.wscommonbnd.TrustedIDEvaluator",
    "com.ibm.etools.webservice.wscommonbnd.TrustedIDEvaluatorRef",
    "com.ibm.etools.webservice.wscommonbnd.ValueType",
    "com.ibm.etools.webservice.wscommonbnd.X509Certificate",
    "com.ibm.etools.webservice.wscommonext.AddCreatedTimeStamp",
    "com.ibm.etools.webservice.wscommonext.AddReceivedTimestamp",
    "com.ibm.etools.webservice.wscommonext.AddTimestamp",
    "com.ibm.etools.webservice.wscommonext.AuthMethod",
    "com.ibm.etools.webservice.wscommonext.Caller",
    "com.ibm.etools.webservice.wscommonext.ConfidentialPart",
    "com.ibm.etools.webservice.wscommonext.Confidentiality",
    "com.ibm.etools.webservice.wscommonext.IDAssertion",
    "com.ibm.etools.webservice.wscommonext.Integrity",
    "com.ibm.etools.webservice.wscommonext.MessageParts",
    "com.ibm.etools.webservice.wscommonext.Nonce",
    "com.ibm.etools.webservice.wscommonext.Reference",
    "com.ibm.etools.webservice.wscommonext.RequiredConfidentiality",
    "com.ibm.etools.webservice.wscommonext.RequiredIntegrity",
    "com.ibm.etools.webservice.wscommonext.RequiredSecurityToken",
    "com.ibm.etools.webservice.wscommonext.SecurityToken",
    "com.ibm.etools.webservice.wscommonext.Timestamp",
    "com.ibm.etools.webservice.wscommonext.TrustMethod",
    "com.ibm.etools.webservice.wsext.LoginConfig",
    "com.ibm.etools.webservice.wsext.PcBinding",
    "com.ibm.etools.webservice.wsext.SecurityRequestConsumerServiceConfig",
    "com.ibm.etools.webservice.wsext.SecurityRequestReceiverServiceConfig",
    "com.ibm.etools.webservice.wsext.SecurityResponseGeneratorServiceConfig",
    "com.ibm.etools.webservice.wsext.SecurityResponseSenderServiceConfig",
    "com.ibm.etools.webservice.wsext.ServerServiceConfig",
    "com.ibm.etools.webservice.wsext.WsDescExt",
    "com.ibm.etools.webservice.wsext.WsExtension",
    "com.ibm.etools.webservice.wssecurity.Binding",
    "com.ibm.etools.webservice.wssecurity.Commonbindings",
    "com.ibm.etools.webservice.wssecurity.Consumer",
    "com.ibm.etools.webservice.wssecurity.Consumerbinding",
    "com.ibm.etools.webservice.wssecurity.Defaultbindings",
    "com.ibm.etools.webservice.wssecurity.Generator",
    "com.ibm.etools.webservice.wssecurity.Generatorbinding",
    "com.ibm.etools.webservice.wssecurity.WSSecurity",
    "com.ibm.websphere.models.config.intellmgmt.Connector",
]
""" Actual types, stored in a separate variable ONLY to trick mkdocs-docstring into showing only the shorter alias. """


ObjectType = _ObjectType
""" List of all the available `wsadmin` object types, as returned by the [`AdminConfig.types()`][wsadmin_type_hints.AdminConfig.types] command.

    !!! Warning 
        Make sure to double check on your system if your **Jython version** has any differences.

    !!! abstract "See also"
        - [`AdminConfig.defaults()`][wsadmin_type_hints.AdminConfig.defaults] ➡ List all the **default values** for all the attributes of a configuration object of the given type;
        - [`AdminConfig.getObjectType()`][wsadmin_type_hints.AdminConfig.getObjectType] ➡ Find the **object type** of an existing configuration **object**;
        - [`AdminConfig.list()`][wsadmin_type_hints.AdminConfig.list] ➡ List all **configuration objects** of a given type;
        - [`AdminConfig.required()`][wsadmin_type_hints.AdminConfig.required] ➡ List all the **required attributes** of an object of the given type;
        - [`AdminConfig.types()`][wsadmin_type_hints.AdminConfig.types] ➡ List all the **available object types**;

    - `AccessPointGroup`
    - `Action`
    - `ActivationSpec`
    - `ActivationSpecTemplateProps`
    - `ActiveAffinityType`
    - `ActivitySessionService`
    - `AdminAgentRegistration`
    - `AdminObject`
    - `AdminObjectTemplateProps`
    - `AdminServerAuthentication`
    - `AdminService`
    - `AdministeredObjectResource`
    - `AffinityType`
    - `AgeCondition`
    - `Agent`
    - `AllActivePolicy`
    - `AllAuthenticatedUsersExt`
    - `AllAuthenticatedUsersInTrustedRealmsExt`
    - `AppAudit`
    - `AppPlacementController`
    - `AppSecurity`
    - `Application`
    - `ApplicationClientFile`
    - `ApplicationConfig`
    - `ApplicationContainer`
    - `ApplicationDeployment`
    - `ApplicationManagementService`
    - `ApplicationProfileService`
    - `ApplicationResources`
    - `ApplicationServer`
    - `ApplicationServerClusterMapping`
    - `ApplicationServerClusterMember`
    - `ApplicationServerEndpoint`
    - `ApplicationServerMapping`
    - `ApplicationServerRoute`
    - `ApplicationServerTimeMapping`
    - `Archive`
    - `Audit`
    - `AuditCommon`
    - `AuditEventFactory`
    - `AuditNotificationMonitor`
    - `AuditPolicy`
    - `AuditServiceProvider`
    - `AuditSpecification`
    - `AuthConfigProvider`
    - `AuthConfigProviderEntry`
    - `AuthMechanism`
    - `AuthModule`
    - `AuthenticationMechanism`
    - `AuthenticationTarget`
    - `AuthorizationConfig`
    - `AuthorizationGroup`
    - `AuthorizationGroupMember`
    - `AuthorizationProvider`
    - `AuthorizationTableExt`
    - `AuthorizationTableImpl`
    - `AutonomicRequestFlowManager`
    - `AverageResponseTimeGoal`
    - `BackupCluster`
    - `BridgeInterface`
    - `CACertificate`
    - `CAClient`
    - `CMPConnectorFactory`
    - `CORBAObjectNameSpaceBinding`
    - `CacheInstance`
    - `CacheInstanceService`
    - `CacheProvider`
    - `CachingAction`
    - `Cell`
    - `CellManager`
    - `CellRoute`
    - `Certificate`
    - `Chain`
    - `Checkpoint`
    - `CheckpointDocument`
    - `Classloader`
    - `ClientModuleDeployment`
    - `ClientModuleRef`
    - `ClusterAddressEndPoint`
    - `ClusterAddressProperties`
    - `ClusterAdvisor`
    - `ClusterMember`
    - `ClusteredTarget`
    - `CommonSecureInterop`
    - `CompatibilityDescriptionGroup`
    - `CompensationService`
    - `CompletionTimeGoal`
    - `Component`
    - `CompressionAction`
    - `ConfigProperty`
    - `ConfigSynchronizationService`
    - `ConnectionDefTemplateProps`
    - `ConnectionDefinition`
    - `ConnectionFactory`
    - `ConnectionFactoryResource`
    - `ConnectionPool`
    - `ConnectionTest`
    - `Connector`
    - `ConnectorCluster`
    - `ConnectorModuleDeployment`
    - `ConnectorModuleRef`
    - `Container`
    - `ContentMapping`
    - `Contributor`
    - `Cookie`
    - `CookieMapping`
    - `CoreGroup`
    - `CoreGroupAccessPoint`
    - `CoreGroupBridgeService`
    - `CoreGroupBridgeSettings`
    - `CoreGroupServer`
    - `CryptoHardwareToken`
    - `CustomAdvisor`
    - `CustomAdvisorMapping`
    - `CustomAdvisorPolicy`
    - `CustomAuthMechanism`
    - `CustomConditionTemplate`
    - `CustomConditionTemplates`
    - `CustomElasticityAction`
    - `CustomErrorPagePolicy`
    - `CustomHealthAction`
    - `CustomProcessDefs`
    - `CustomService`
    - `CustomUserRegistry`
    - `DCSInboundChannel`
    - `DPClonableDeviceSettings`
    - `DPClonableDeviceSettingsVersion`
    - `DPDeployableConfiguration`
    - `DPDevice`
    - `DPDomain`
    - `DPDomainVersion`
    - `DPFirmware`
    - `DPFirmwareVersion`
    - `DPManagedSet`
    - `DPManager`
    - `DPVersion`
    - `DRSConnectionPool`
    - `DRSPartition`
    - `DRSSerialization`
    - `DRSSettings`
    - `DataPowerMgrInboundChannel`
    - `DataReplication`
    - `DataReplicationDomain`
    - `DataSource`
    - `DataSourceDefinition`
    - `DebugService`
    - `DefaultSIPApplicationRouter`
    - `DeployedMiddlewareApp`
    - `DeployedMiddlewareAppEdition`
    - `DeployedObject`
    - `DeployedObjectConfig`
    - `DeployedObjectProxyConfig`
    - `Deployment`
    - `DeploymentTarget`
    - `DeploymentTargetMapping`
    - `Description`
    - `DescriptionGroup`
    - `DescriptiveProperty`
    - `DescriptivePropertyGroup`
    - `DiagnosticProviderService`
    - `DigestAuthentication`
    - `DiscoverableDescriptiveProperty`
    - `DiscretionaryGoal`
    - `DiskCacheCustomPerformanceSettings`
    - `DiskCacheEvictionPolicy`
    - `DisplayDescriptor`
    - `DisplayName`
    - `DynamicCache`
    - `DynamicCluster`
    - `DynamicReload`
    - `DynamicSSLConfigSelection`
    - `DynamicWtCtrlr`
    - `EARFile`
    - `EJBAsync`
    - `EJBCache`
    - `EJBContainer`
    - `EJBDeployment`
    - `EJBJarFile`
    - `EJBLocalRef`
    - `EJBModuleConfiguration`
    - `EJBModuleDeployment`
    - `EJBModuleRef`
    - `EJBTimer`
    - `EjbNameSpaceBinding`
    - `EjbRef`
    - `ElasticityAction`
    - `ElasticityClass`
    - `ElasticityCustomProcessDefs`
    - `ElasticityType`
    - `EmailNotifications`
    - `EndPoint`
    - `EndPointRef`
    - `EnterpriseBeanConfig`
    - `EnvEntry`
    - `ErrorMapping`
    - `EveryoneExt`
    - `ExecutionTimeAndThreadLimit`
    - `ExtendedApplicationData`
    - `ExtendedRepositoryService`
    - `Extension`
    - `ExtensionMBean`
    - `ExtensionMBeanProvider`
    - `ExternalCacheGroup`
    - `ExternalCacheGroupMember`
    - `ExternalDomain`
    - `ExternalFile`
    - `ExternalFileService`
    - `ExternallyManagedHTTPServer`
    - `FRCACacheGroupMember`
    - `FailRoute`
    - `File`
    - `FileTransferService`
    - `Filter`
    - `ForeignCell`
    - `ForeignServer`
    - `GCPercentageCondition`
    - `GSCMember`
    - `GSCMemberEndpoint`
    - `GenericChannelData`
    - `GenericChannelFactory`
    - `GenericClusterRoute`
    - `GenericInboundChannel`
    - `GenericJMSConnectionFactory`
    - `GenericJMSDestination`
    - `GenericOutboundChannel`
    - `GenericServerCluster`
    - `GenericServerClusterMapping`
    - `GenericServerClusterRoute`
    - `GenericServerClusterTimeMapping`
    - `GenericServerEndpoint`
    - `GridClassRules`
    - `GridMatchRule`
    - `GridScheduler`
    - `GridWorkGoal`
    - `GroupExt`
    - `HAManagerPolicy`
    - `HAManagerService`
    - `HPELLog`
    - `HPELTextLog`
    - `HPELTrace`
    - `HTTPAccessLoggingService`
    - `HTTPConnector`
    - `HTTPInboundChannel`
    - `HTTPInboundChannelLogging`
    - `HTTPOutboundChannel`
    - `HTTPProxyServerSettings`
    - `HTTPQueueInboundChannel`
    - `HTTPRequestCompressionAction`
    - `HTTPRequestHeaderAction`
    - `HTTPResponseCompressionAction`
    - `HTTPResponseHeaderAction`
    - `HTTPTransport`
    - `HTTPTunnelInboundChannel`
    - `HTTPTunnelOutboundChannel`
    - `HeaderAction`
    - `HeaderCondition`
    - `HealthAction`
    - `HealthClass`
    - `HealthCondition`
    - `HealthController`
    - `HealthTime`
    - `HighPerformanceExtensibleLogging`
    - `HostAlias`
    - `I18NService`
    - `IIOPLayer`
    - `IIOPSecurityProtocol`
    - `IIOPTransport`
    - `IPCConnector`
    - `IPSprayer`
    - `IconType`
    - `Identity`
    - `IdentityAssertionLayer`
    - `IdentityAssertionQOP`
    - `IdentityAssertionTypeAssociation`
    - `InboundResourceAdapter`
    - `InboundTransportChannel`
    - `IndirectLookupNameSpaceBinding`
    - `InjectionTarget`
    - `InstancePool`
    - `IntelligentManagement`
    - `Interceptor`
    - `InvalidationSchedule`
    - `J2CActivationSpec`
    - `J2CAdminObject`
    - `J2CConnectionFactory`
    - `J2CResourceAdapter`
    - `J2EEEAttribute`
    - `J2EEEObject`
    - `J2EEResourceFactory`
    - `J2EEResourceProperty`
    - `J2EEResourcePropertySet`
    - `J2EEResourceProvider`
    - `JAASAuthData`
    - `JAASConfiguration`
    - `JAASConfigurationEntry`
    - `JAASLoginModule`
    - `JASPIConfiguration`
    - `JAXRPCHandler`
    - `JAXRPCHandlerList`
    - `JAXRPCHeader`
    - `JAXWSHandler`
    - `JAXWSHandlerList`
    - `JDBCProvider`
    - `JFAPFactory`
    - `JFAPInboundChannel`
    - `JFAPOutboundChannel`
    - `JMSConnectionFactory`
    - `JMSConnectionFactoryResource`
    - `JMSConnector`
    - `JMSDestination`
    - `JMSDestinationResource`
    - `JMSProvider`
    - `JMSServer`
    - `JMSTransport`
    - `JMXConnector`
    - `JNDIEnvRefsGroup`
    - `JSR160RMIConnector`
    - `JavaEEDefaultResources`
    - `JavaPersistenceAPIService`
    - `JavaProcessDef`
    - `JavaVirtualMachine`
    - `JavaVirtualMachinePreset`
    - `JobClass`
    - `JobLogLimit`
    - `JobManager`
    - `JobManagerRegistration`
    - `KRB5`
    - `Key`
    - `KeyManager`
    - `KeyReference`
    - `KeySet`
    - `KeySetGroup`
    - `KeyStore`
    - `KeyStoreFile`
    - `LDAPSearchFilter`
    - `LDAPUserRegistry`
    - `LSDConnection`
    - `LTPA`
    - `Library`
    - `LibraryRef`
    - `License`
    - `LifecycleCallbackType`
    - `Listener`
    - `ListenerPort`
    - `Liveness`
    - `LocalErrorPagePolicy`
    - `LocalOSUserRegistry`
    - `LocalRoute`
    - `LogFile`
    - `LooseApplication`
    - `LooseArchive`
    - `LooseArchiveMetadata`
    - `LooseConfiguration`
    - `LooseLibrary`
    - `LooseModule`
    - `LooseWARFile`
    - `MOfNPolicy`
    - `MQConnectionFactory`
    - `MQFAPInboundChannel`
    - `MQFAPOutboundChannel`
    - `MQQueue`
    - `MQQueueConnectionFactory`
    - `MQTopic`
    - `MQTopicConnectionFactory`
    - `MailProvider`
    - `MailSession`
    - `MailSessionResource`
    - `ManagedMiddlewareAppEdition`
    - `ManagedNode`
    - `ManagedObject`
    - `ManagementScope`
    - `MappingModule`
    - `MatchCriteria`
    - `MatchRule`
    - `MemoryCacheEvictionPolicy`
    - `MemoryCondition`
    - `MemoryLeakAlgorithm`
    - `MessageAdapter`
    - `MessageCondition`
    - `MessageDestination`
    - `MessageDestinationRef`
    - `MessageLayer`
    - `MessageListener`
    - `MessageListenerService`
    - `MessageQOP`
    - `MethodMessageCondition`
    - `MiddlewareApp`
    - `MiddlewareAppEdition`
    - `MiddlewareAppScript`
    - `MiddlewareClusterTarget`
    - `MiddlewareDescriptor`
    - `MiddlewareModule`
    - `MiddlewareServerTarget`
    - `MiddlewareTarget`
    - `MiddlewareVersionDescriptor`
    - `MiddlewareWebModule`
    - `MimeEntry`
    - `ModuleConfig`
    - `ModuleDeployment`
    - `ModuleFile`
    - `ModuleRef`
    - `ModuleShare`
    - `MonitoredDirectoryDeployment`
    - `MonitoringPolicy`
    - `MultiBrokerRoutingEntry`
    - `MultiCellOverlayBridge`
    - `MultibrokerDomain`
    - `NameBinding`
    - `NameServer`
    - `NameSpaceBinding`
    - `NamedEndPoint`
    - `NamedJavaProcessDef`
    - `NamedProcessDef`
    - `NamingContext`
    - `NewClass`
    - `NoOpPolicy`
    - `Node`
    - `NodeAgent`
    - `NodeGroup`
    - `NodeGroupMember`
    - `OLTPWorkGoal`
    - `ORBInboundChannel`
    - `ORBPlugin`
    - `ObjectCacheInstance`
    - `ObjectPool`
    - `ObjectPoolManagerInfo`
    - `ObjectPoolProvider`
    - `ObjectPoolService`
    - `ObjectRequestBroker`
    - `OnDemandRouter`
    - `OneOfNPolicy`
    - `OutboundResourceAdapter`
    - `OutboundTransportChannel`
    - `OutputQueueLimit`
    - `OutputRedirect`
    - `OverlayEndpoint`
    - `PME502ServerExtension`
    - `PME51ServerExtension`
    - `PMEClusterExtension`
    - `PMEServerExtension`
    - `PMIModule`
    - `PMIRMFilter`
    - `PMIRMFilterValue`
    - `PMIRequestMetrics`
    - `PMIService`
    - `ParamValue`
    - `PassiveAffinityType`
    - `PeerAccessPoint`
    - `PeerCoreGroup`
    - `PercentileResponseTimeGoal`
    - `PerformanceGoal`
    - `PersistenceContextRef`
    - `PersistenceUnitRef`
    - `PluginConfigPolicy`
    - `PluginConfigService`
    - `PluginProperties`
    - `PluginServerClusterProperties`
    - `Policy`
    - `PortletContainer`
    - `PreferenceSet`
    - `Preferences`
    - `PreferredServerPolicy`
    - `PrimaryAdminExt`
    - `ProcessDef`
    - `ProcessExecution`
    - `Property`
    - `PropertySet`
    - `ProtocolProvider`
    - `Proxy`
    - `ProxyAction`
    - `ProxyInboundChannel`
    - `ProxyOverrides`
    - `ProxyRuleExpression`
    - `ProxyServer`
    - `ProxySettings`
    - `ProxyVirtualHost`
    - `ProxyVirtualHostConfig`
    - `ProxyVirtualHostSettings`
    - `QName`
    - `QualityOfProtection`
    - `QueueTimeGoal`
    - `RARFile`
    - `RASLoggingService`
    - `RMIConnector`
    - `RMQChannelFactory`
    - `RMQOutboundChannel`
    - `RSAToken`
    - `ReadOnlyDirectory`
    - `RecoveryLog`
    - `RedirectRoute`
    - `Referenceable`
    - `RemoteCellAccessPoint`
    - `RemoteCellOverrides`
    - `RepositoryService`
    - `RequiredConfigPropertyType`
    - `ResourceAdapter`
    - `ResourceEnvEntry`
    - `ResourceEnvRef`
    - `ResourceEnvironmentProvider`
    - `ResourceRef`
    - `ResponseCondition`
    - `RestartTime`
    - `RewritingAction`
    - `RewritingPolicy`
    - `RewritingRule`
    - `RoleAssignmentExt`
    - `RoleBasedAuthorization`
    - `Route`
    - `RoutingAction`
    - `RoutingPolicy`
    - `RoutingRule`
    - `Rule`
    - `Rules`
    - `Ruleset`
    - `RunAsSpecifiedIdentity`
    - `SARClusterTarget`
    - `SARDeploymentTarget`
    - `SARServerTarget`
    - `SIBAbstractDestination`
    - `SIBAudit`
    - `SIBAuthAlias`
    - `SIBAuthBrowser`
    - `SIBAuthBusConnect`
    - `SIBAuthCreator`
    - `SIBAuthDefault`
    - `SIBAuthForeignBus`
    - `SIBAuthForeignDestination`
    - `SIBAuthGroup`
    - `SIBAuthIdentityAdopter`
    - `SIBAuthPort`
    - `SIBAuthQueue`
    - `SIBAuthReceiver`
    - `SIBAuthSender`
    - `SIBAuthSpace`
    - `SIBAuthTopic`
    - `SIBAuthTopicSpace`
    - `SIBAuthTopicSpaceBase`
    - `SIBAuthTopicSpaceRoot`
    - `SIBAuthUser`
    - `SIBAuthWebService`
    - `SIBBootstrapMember`
    - `SIBContextInfo`
    - `SIBDatastore`
    - `SIBDestination`
    - `SIBDestinationAlias`
    - `SIBDestinationDefault`
    - `SIBDestinationForeign`
    - `SIBDestinationMediation`
    - `SIBDestinationMediationRef`
    - `SIBFilestore`
    - `SIBForeignBus`
    - `SIBGatewayLink`
    - `SIBJMSConnectionFactory`
    - `SIBJMSProvider`
    - `SIBJMSQueue`
    - `SIBJMSQueueConnectionFactory`
    - `SIBJMSTopic`
    - `SIBJMSTopicConnectionFactory`
    - `SIBLinkRef`
    - `SIBLocalizationPoint`
    - `SIBLocalizationPointRef`
    - `SIBMQClientLink`
    - `SIBMQClientLinkAdvancedProperties`
    - `SIBMQLink`
    - `SIBMQLinkReceiverChannel`
    - `SIBMQLinkSenderChannel`
    - `SIBMQLinkSenderChannelLocalizationPoint`
    - `SIBMQLocalizationPointProxy`
    - `SIBMQMediationPointProxy`
    - `SIBMQQueueLocalizationPointProxy`
    - `SIBMQServer`
    - `SIBMQServerBusMember`
    - `SIBMediation`
    - `SIBMediationExecutionPoint`
    - `SIBMediationInstance`
    - `SIBMediationLocalizationPoint`
    - `SIBMessagingEngine`
    - `SIBPSBBrokerProfile`
    - `SIBPSBBrokerTransactionality`
    - `SIBPSBTopicMapping`
    - `SIBPSBTopicTransactionality`
    - `SIBPermittedChain`
    - `SIBPort`
    - `SIBQualifiedDestinationName`
    - `SIBQueue`
    - `SIBQueueLocalizationPoint`
    - `SIBService`
    - `SIBTopicSpace`
    - `SIBTopicSpaceAudit`
    - `SIBTopicSpaceLocalizationPoint`
    - `SIBTopicSpaceMapEntry`
    - `SIBTopicSpaceMapping`
    - `SIBVirtualGatewayLink`
    - `SIBVirtualLink`
    - `SIBVirtualMQLink`
    - `SIBWMQServerEndpoint`
    - `SIBWMQServerSvrconnChannel`
    - `SIBWSBusConnectionProperty`
    - `SIBWSEndpointListener`
    - `SIBWSEndpointListenerReference`
    - `SIBWSInboundPort`
    - `SIBWSInboundPortReference`
    - `SIBWSInboundService`
    - `SIBWSOutboundPort`
    - `SIBWSOutboundService`
    - `SIBWSSecurityInboundConfig`
    - `SIBWSSecurityOutboundConfig`
    - `SIBWSSecurityRequestConsumerBindingConfig`
    - `SIBWSSecurityRequestGeneratorBindingConfig`
    - `SIBWSSecurityRequestReceiverBindingConfig`
    - `SIBWSSecurityRequestSenderBindingConfig`
    - `SIBWSSecurityResponseConsumerBindingConfig`
    - `SIBWSSecurityResponseGeneratorBindingConfig`
    - `SIBWSSecurityResponseReceiverBindingConfig`
    - `SIBWSSecurityResponseSenderBindingConfig`
    - `SIBWSUDDIPublication`
    - `SIBWSWSDLLocation`
    - `SIBWebService`
    - `SIBus`
    - `SIBusMember`
    - `SIBusMemberTarget`
    - `SIPApplicationRouter`
    - `SIPApplicationRouters`
    - `SIPContainer`
    - `SIPContainerInboundChannel`
    - `SIPInboundChannel`
    - `SIPMessageCondition`
    - `SIPOutboundChannel`
    - `SIPProxyInboundChannel`
    - `SIPProxyServerSettings`
    - `SIPProxySettings`
    - `SIPRoutingRule`
    - `SOAPConnector`
    - `SPNEGO`
    - `SSLConfig`
    - `SSLConfigGroup`
    - `SSLInboundChannel`
    - `SSLOutboundChannel`
    - `SWAMAuthentication`
    - `SchedulerConfiguration`
    - `SchedulerProvider`
    - `SchedulerService`
    - `SecureAssociationService`
    - `SecureClusterAddressEndPoint`
    - `SecureSessionCookie`
    - `SecureSocketLayer`
    - `Security`
    - `SecurityCommon`
    - `SecurityDomain`
    - `SecurityDomainMember`
    - `SecurityIdentity`
    - `SecurityPermission`
    - `SecurityProtocolConfig`
    - `SecurityProtocolQOP`
    - `SecurityRole`
    - `SecurityRoleExt`
    - `SecurityRoleRef`
    - `SecurityServer`
    - `Server`
    - `ServerCluster`
    - `ServerComponent`
    - `ServerEntry`
    - `ServerExt`
    - `ServerIdentity`
    - `ServerIndex`
    - `ServerInstance`
    - `ServerTarget`
    - `Service`
    - `ServiceClass`
    - `ServiceClassGoal`
    - `ServiceContext`
    - `ServiceLog`
    - `ServletCacheInstance`
    - `SessionBeanConfig`
    - `SessionDatabasePersistence`
    - `SessionManager`
    - `SessionSecurity`
    - `SingleSignon`
    - `SpecialSubjectExt`
    - `Stack`
    - `StandAloneApplicationServerMapping`
    - `StartupBeansService`
    - `StateManageable`
    - `StatefulSessionBeanConfig`
    - `StaticCachePolicy`
    - `StaticCacheRule`
    - `StaticFileServingPolicy`
    - `StaticPolicy`
    - `StatisticsProvider`
    - `StormDrainCondition`
    - `StreamRedirect`
    - `StringNameSpaceBinding`
    - `StuckRequestCondition`
    - `SubjectExt`
    - `SystemMessageServer`
    - `TAInterceptor`
    - `TCPFactory`
    - `TCPInboundChannel`
    - `TCPOutboundChannel`
    - `TPVService`
    - `TargetMembership`
    - `TaskProvider`
    - `ThreadPool`
    - `ThreadPoolManager`
    - `TimeMapping`
    - `TimerManagerInfo`
    - `TimerManagerProvider`
    - `Timers`
    - `TivoliPerfViewer`
    - `TraceLog`
    - `TraceService`
    - `TraceSpecification`
    - `TransactionClass`
    - `TransactionClassModule`
    - `TransactionService`
    - `Transport`
    - `TransportChannel`
    - `TransportChannelFactory`
    - `TransportChannelService`
    - `TransportLayer`
    - `TransportQOP`
    - `TrustAssociation`
    - `TrustManager`
    - `TrustedAuthenticationRealm`
    - `TuningParams`
    - `TunnelAccessPointGroup`
    - `TunnelPeerAccessPoint`
    - `TunnelTemplate`
    - `TypedProperty`
    - `UDDIConfig`
    - `UDDIReference`
    - `UDPInboundChannel`
    - `UDPOutboundChannel`
    - `URIGroup`
    - `URL`
    - `URLProvider`
    - `UnmanagedMiddlewareAppEdition`
    - `UseCallerIdentity`
    - `UserDefinedLine`
    - `UserExt`
    - `UserRegistry`
    - `VariableMap`
    - `VariableSubstitutionEntry`
    - `VirtualHost`
    - `VisualizationDataLog`
    - `VisualizationDataService`
    - `WARFile`
    - `WARFragmentFile`
    - `WAS40ConnectionPool`
    - `WAS40DataSource`
    - `WASAbstractAuthData`
    - `WASAddressingType`
    - `WASAdministeredObjectResource`
    - `WASBasicAuthData`
    - `WASConnectionFactoryResource`
    - `WASDataSourceDefinition`
    - `WASDataSourceDefinitionBinding`
    - `WASEjbRef`
    - `WASEjbRefBinding`
    - `WASEnvEntry`
    - `WASHandler`
    - `WASHandlerChain`
    - `WASHandlerChains`
    - `WASJMSConnectionFactoryResource`
    - `WASJMSDestinationResource`
    - `WASMailSessionResource`
    - `WASMessageDestinationRef`
    - `WASMessageDestinationRefBinding`
    - `WASParamValue`
    - `WASPersistenceContextRef`
    - `WASPersistenceUnitRef`
    - `WASPortComponentRef`
    - `WASQName`
    - `WASQueue`
    - `WASQueueConnectionFactory`
    - `WASResourceEnvRef`
    - `WASResourceEnvRefBinding`
    - `WASResourceRef`
    - `WASResourceRefBinding`
    - `WASResourceRefExtension`
    - `WASRespectBindingType`
    - `WASServiceRef`
    - `WASTopic`
    - `WASTopicConnectionFactory`
    - `WIMUserRegistry`
    - `WLMCoreGroupBridgePlugin`
    - `WSByteBufferService`
    - `WSCertificateExpirationMonitor`
    - `WSGWGatewayService`
    - `WSGWInstance`
    - `WSGWProxyService`
    - `WSGWTargetService`
    - `WSNAdministeredSubscriber`
    - `WSNInstanceDocument`
    - `WSNService`
    - `WSNServicePoint`
    - `WSNTopicNamespace`
    - `WSNotification`
    - `WSPassword`
    - `WSPasswordEncryption`
    - `WSPasswordLocator`
    - `WSSchedule`
    - `WSSecurityScannerMonitor`
    - `WebContainer`
    - `WebContainerInboundChannel`
    - `WebModuleConfig`
    - `WebModuleDeployment`
    - `WebModuleRef`
    - `WebServer`
    - `WebserverPluginSettings`
    - `WeightAdvisor`
    - `WorkAreaPartition`
    - `WorkAreaPartitionService`
    - `WorkAreaService`
    - `WorkClass`
    - `WorkClassModule`
    - `WorkManagerInfo`
    - `WorkManagerProvider`
    - `WorkManagerService`
    - `WorkloadCondition`
    - `WorkloadManagementPolicy`
    - `WorkloadManagementServer`
    - `com.ibm.etools.webservice.wsbnd.DefaultEndpointURIPrefix`
    - `com.ibm.etools.webservice.wsbnd.PCBinding`
    - `com.ibm.etools.webservice.wsbnd.RouterModule`
    - `com.ibm.etools.webservice.wsbnd.SecurityRequestConsumerBindingConfig`
    - `com.ibm.etools.webservice.wsbnd.SecurityRequestReceiverBindingConfig`
    - `com.ibm.etools.webservice.wsbnd.SecurityResponseGeneratorBindingConfig`
    - `com.ibm.etools.webservice.wsbnd.SecurityResponseSenderBindingConfig`
    - `com.ibm.etools.webservice.wsbnd.WSBinding`
    - `com.ibm.etools.webservice.wsbnd.WSDescBinding`
    - `com.ibm.etools.webservice.wscbnd.BasicAuth`
    - `com.ibm.etools.webservice.wscbnd.ClientBinding`
    - `com.ibm.etools.webservice.wscbnd.ComponentScopedRefs`
    - `com.ibm.etools.webservice.wscbnd.DefaultMapping`
    - `com.ibm.etools.webservice.wscbnd.LoginBinding`
    - `com.ibm.etools.webservice.wscbnd.PortQnameBinding`
    - `com.ibm.etools.webservice.wscbnd.SecurityRequestGeneratorBindingConfig`
    - `com.ibm.etools.webservice.wscbnd.SecurityRequestSenderBindingConfig`
    - `com.ibm.etools.webservice.wscbnd.SecurityResponseConsumerBindingConfig`
    - `com.ibm.etools.webservice.wscbnd.SecurityResponseReceiverBindingConfig`
    - `com.ibm.etools.webservice.wscbnd.ServiceRef`
    - `com.ibm.etools.webservice.wscext.ClientServiceConfig`
    - `com.ibm.etools.webservice.wscext.ComponentScopedRefs`
    - `com.ibm.etools.webservice.wscext.DefaultMapping`
    - `com.ibm.etools.webservice.wscext.LoginConfig`
    - `com.ibm.etools.webservice.wscext.PortQnameBinding`
    - `com.ibm.etools.webservice.wscext.SecurityRequestGeneratorServiceConfig`
    - `com.ibm.etools.webservice.wscext.SecurityRequestSenderServiceConfig`
    - `com.ibm.etools.webservice.wscext.SecurityResponseConsumerServiceConfig`
    - `com.ibm.etools.webservice.wscext.SecurityResponseReceiverServiceConfig`
    - `com.ibm.etools.webservice.wscext.ServiceRef`
    - `com.ibm.etools.webservice.wscext.WsClientExtension`
    - `com.ibm.etools.webservice.wscommonbnd.AlgorithmMapping`
    - `com.ibm.etools.webservice.wscommonbnd.AlgorithmURI`
    - `com.ibm.etools.webservice.wscommonbnd.CRL`
    - `com.ibm.etools.webservice.wscommonbnd.CallbackHandler`
    - `com.ibm.etools.webservice.wscommonbnd.CallbackHandlerFactory`
    - `com.ibm.etools.webservice.wscommonbnd.CanonicalizationMethod`
    - `com.ibm.etools.webservice.wscommonbnd.CertPathSettings`
    - `com.ibm.etools.webservice.wscommonbnd.CertStoreList`
    - `com.ibm.etools.webservice.wscommonbnd.CertStoreRef`
    - `com.ibm.etools.webservice.wscommonbnd.CollectionCertStore`
    - `com.ibm.etools.webservice.wscommonbnd.Consumerbindingref`
    - `com.ibm.etools.webservice.wscommonbnd.DataEncryptionMethod`
    - `com.ibm.etools.webservice.wscommonbnd.DigestMethod`
    - `com.ibm.etools.webservice.wscommonbnd.EncryptionInfo`
    - `com.ibm.etools.webservice.wscommonbnd.EncryptionKey`
    - `com.ibm.etools.webservice.wscommonbnd.EncryptionKeyInfo`
    - `com.ibm.etools.webservice.wscommonbnd.Generatorbindingref`
    - `com.ibm.etools.webservice.wscommonbnd.JAASConfig`
    - `com.ibm.etools.webservice.wscommonbnd.KeyEncryptionMethod`
    - `com.ibm.etools.webservice.wscommonbnd.KeyInfo`
    - `com.ibm.etools.webservice.wscommonbnd.KeyInfoSignature`
    - `com.ibm.etools.webservice.wscommonbnd.KeyLocator`
    - `com.ibm.etools.webservice.wscommonbnd.KeyLocatorMapping`
    - `com.ibm.etools.webservice.wscommonbnd.KeyStore`
    - `com.ibm.etools.webservice.wscommonbnd.LDAPCertStore`
    - `com.ibm.etools.webservice.wscommonbnd.LDAPServer`
    - `com.ibm.etools.webservice.wscommonbnd.LoginMapping`
    - `com.ibm.etools.webservice.wscommonbnd.NonceCaching`
    - `com.ibm.etools.webservice.wscommonbnd.Parameter`
    - `com.ibm.etools.webservice.wscommonbnd.PartReference`
    - `com.ibm.etools.webservice.wscommonbnd.SignatureMethod`
    - `com.ibm.etools.webservice.wscommonbnd.SigningInfo`
    - `com.ibm.etools.webservice.wscommonbnd.SigningKey`
    - `com.ibm.etools.webservice.wscommonbnd.SigningKeyInfo`
    - `com.ibm.etools.webservice.wscommonbnd.TokenConsumer`
    - `com.ibm.etools.webservice.wscommonbnd.TokenGenerator`
    - `com.ibm.etools.webservice.wscommonbnd.TokenReference`
    - `com.ibm.etools.webservice.wscommonbnd.TokenValueType`
    - `com.ibm.etools.webservice.wscommonbnd.Transform`
    - `com.ibm.etools.webservice.wscommonbnd.TrustAnchor`
    - `com.ibm.etools.webservice.wscommonbnd.TrustAnchorRef`
    - `com.ibm.etools.webservice.wscommonbnd.TrustAnyCertificate`
    - `com.ibm.etools.webservice.wscommonbnd.TrustedIDEvaluator`
    - `com.ibm.etools.webservice.wscommonbnd.TrustedIDEvaluatorRef`
    - `com.ibm.etools.webservice.wscommonbnd.ValueType`
    - `com.ibm.etools.webservice.wscommonbnd.X509Certificate`
    - `com.ibm.etools.webservice.wscommonext.AddCreatedTimeStamp`
    - `com.ibm.etools.webservice.wscommonext.AddReceivedTimestamp`
    - `com.ibm.etools.webservice.wscommonext.AddTimestamp`
    - `com.ibm.etools.webservice.wscommonext.AuthMethod`
    - `com.ibm.etools.webservice.wscommonext.Caller`
    - `com.ibm.etools.webservice.wscommonext.ConfidentialPart`
    - `com.ibm.etools.webservice.wscommonext.Confidentiality`
    - `com.ibm.etools.webservice.wscommonext.IDAssertion`
    - `com.ibm.etools.webservice.wscommonext.Integrity`
    - `com.ibm.etools.webservice.wscommonext.MessageParts`
    - `com.ibm.etools.webservice.wscommonext.Nonce`
    - `com.ibm.etools.webservice.wscommonext.Reference`
    - `com.ibm.etools.webservice.wscommonext.RequiredConfidentiality`
    - `com.ibm.etools.webservice.wscommonext.RequiredIntegrity`
    - `com.ibm.etools.webservice.wscommonext.RequiredSecurityToken`
    - `com.ibm.etools.webservice.wscommonext.SecurityToken`
    - `com.ibm.etools.webservice.wscommonext.Timestamp`
    - `com.ibm.etools.webservice.wscommonext.TrustMethod`
    - `com.ibm.etools.webservice.wsext.LoginConfig`
    - `com.ibm.etools.webservice.wsext.PcBinding`
    - `com.ibm.etools.webservice.wsext.SecurityRequestConsumerServiceConfig`
    - `com.ibm.etools.webservice.wsext.SecurityRequestReceiverServiceConfig`
    - `com.ibm.etools.webservice.wsext.SecurityResponseGeneratorServiceConfig`
    - `com.ibm.etools.webservice.wsext.SecurityResponseSenderServiceConfig`
    - `com.ibm.etools.webservice.wsext.ServerServiceConfig`
    - `com.ibm.etools.webservice.wsext.WsDescExt`
    - `com.ibm.etools.webservice.wsext.WsExtension`
    - `com.ibm.etools.webservice.wssecurity.Binding`
    - `com.ibm.etools.webservice.wssecurity.Commonbindings`
    - `com.ibm.etools.webservice.wssecurity.Consumer`
    - `com.ibm.etools.webservice.wssecurity.Consumerbinding`
    - `com.ibm.etools.webservice.wssecurity.Defaultbindings`
    - `com.ibm.etools.webservice.wssecurity.Generator`
    - `com.ibm.etools.webservice.wssecurity.Generatorbinding`
    - `com.ibm.etools.webservice.wssecurity.WSSecurity`
    - `com.ibm.websphere.models.config.intellmgmt.Connector`
"""