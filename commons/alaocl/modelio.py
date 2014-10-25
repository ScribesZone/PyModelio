# coding=utf-8

__all__ =(
)

import alaocl.injector

# noinspection PyUnresolvedReferences
from org.eclipse.emf.common.util import EList
# noinspection PyUnresolvedReferences
from org.modelio.vcore.smkernel import SmList
# noinspection PyUnresolvedReferences
from org.modelio.vcore.smkernel import SmConstrainedList



# noinspection PyUnresolvedReferences
MODELIO_LISTS = [
    # FIXME: in fact this line  useless as addSuperClass does not works with inheritance
    # noinspection PyUnresolvedReferences
    EList,

    SmList,
    SmConstrainedList,
]

alaocl.injector.addSuperclass(alaocl.jython.JavaListExtension,MODELIO_LISTS)

# http://download.eclipse.org/modeling/emf/emf/javadoc/2.5.0/org/eclipse/emf/common/util/EList.html
# AbstractSequentialInternalEList, AbstractTreeIterator, AdapterFactoryEditingDomain.DomainTreeIterator, AdapterFactoryTreeIterator, BasicEList, BasicEList.FastCompare, BasicEList.UnmodifiableEList, BasicEMap, BasicFeatureMap, BasicInternalEList, BasicNotifierImpl.EAdapterList, ConverterUtil.EPackageList, ConverterUtil.GenPackageList, DelegatingEcoreEList, DelegatingEcoreEList.Dynamic, DelegatingEcoreEList.Generic, DelegatingEcoreEList.UnmodifiableEList, DelegatingEcoreEList.Unsettable, DelegatingEList, DelegatingEList.UnmodifiableEList, DelegatingFeatureMap, DelegatingNotifyingInternalEListImpl, DelegatingNotifyingListImpl, EContentsEList, EcoreEList, EcoreEList.Dynamic, EcoreEList.Generic, EcoreEList.UnmodifiableEList, EcoreEList.UnmodifiableEList.FastCompare, EcoreEMap, EcoreEMap.DelegateEObjectContainmentEList, EcoreEMap.Unsettable, EcoreEMap.Unsettable.UnsettableDelegateEObjectContainmentEList, EcoreUtil.ContentTreeIterator, ECrossReferenceEList, EDataTypeEList, EDataTypeEList.Unsettable, EDataTypeUniqueEList, EDataTypeUniqueEList.Unsettable, EObjectContainmentEList, EObjectContainmentEList.Resolving, EObjectContainmentEList.Unsettable, EObjectContainmentEList.Unsettable.Resolving, EObjectContainmentWithInverseEList, EObjectContainmentWithInverseEList.Resolving, EObjectContainmentWithInverseEList.Unsettable, EObjectContainmentWithInverseEList.Unsettable.Resolving, EObjectEList, EObjectEList.Unsettable, EObjectResolvingEList, EObjectResolvingEList.Unsettable, EObjectWithInverseEList, EObjectWithInverseEList.ManyInverse, EObjectWithInverseEList.Unsettable, EObjectWithInverseEList.Unsettable.ManyInverse, EObjectWithInverseResolvingEList, EObjectWithInverseResolvingEList.ManyInverse, EObjectWithInverseResolvingEList.Unsettable, EObjectWithInverseResolvingEList.Unsettable.ManyInverse, EStoreEObjectImpl.BasicEStoreEList, EStoreEObjectImpl.BasicEStoreFeatureMap, EStoreEObjectImpl.EStoreEList, EStoreEObjectImpl.EStoreFeatureMap, ExtensibleURIConverterImpl.ContentHandlerList, ExtensibleURIConverterImpl.URIHandlerList, FeatureMapUtil.FeatureEList, FeatureMapUtil.FeatureEList.Basic, FeatureMapUtil.FeatureFeatureMap, ItemProvider.ItemProviderNotifyingArrayList, ItemProviderAdapter.ModifiableSingletonEList, MappingImpl.MappingTreeIterator, ModelExporter.GenPackagesTreeIterator, NotificationChainImpl, NotifyingInternalEListImpl, NotifyingListImpl, ResourceImpl.ContentsEList, ResourceSetImpl.ResourcesEList, StringSegment, UniqueEList, UniqueEList.FastCompare, URIMappingRegistryImpl, XMLHandler.MyEObjectStack, XMLHandler.MyStack, XMLString
