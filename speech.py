#import pyttsx
#engine = pyttsx.init()
#engine.say('Good morning.')
#engine.runAndWait()

from AppKit import NSSpeechSynthesizer

print(NSSpeechSynthesizer.availableVoices())
speechSynthesizer = NSSpeechSynthesizer.alloc().initWithVoice_("com.apple.speech.synthesis.voice.karen")
#speechSynthesizer = NSSpeechSynthesizer.alloc().initWithVoice_("com.apple.speech.synthesis.voice.sara")
test = speechSynthesizer.startSpeakingString_('Hi! Nice to meet you! So how are you today? Feeling anxious. Quite normal considering this is your first time in space. I am sure you will get used to zero gravity within a few weeks. We will all be here to help you through these first critical weeks.')
#test = speechSynthesizer.startSpeakingString_('Hej, jeg hedder Sara. Jeg er en dansk stemme.')

def methods(cls):
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]

#print(NSSpeechSynthesizer.__dict__)
#print(methods(NSSpeechSynthesizer))
#print(list(dir(NSSpeechSynthesizer)))
#print(NSSpeechSynthesizer.__dict__.items())

	#attrib = NSSpeechSynthesizer.attributes(voice)
	#print(voice.attributesforVoice())
	#print(type(voice))


#print(dir(voice))
#while speechSynthesizer.isSpeaking:
#	pass

import time

"""
<<say -v "?"

lex                en_US    # Most people recognize me by my voice.
Alice               it_IT    # Salve, mi chiamo Alice e sono una voce italiana.
Alva                sv_SE    # Hej, jag heter Alva. Jag är en svensk röst.
Amelie              fr_CA    # Bonjour, je m’appelle Amelie. Je suis une voix canadienne.
Anna                de_DE    # Hallo, ich heiße Anna und ich bin eine deutsche Stimme.
Carmit              he_IL    # שלום. קוראים לי כרמית, ואני קול בשפה העברית.
Damayanti           id_ID    # Halo, nama saya Damayanti. Saya berbahasa Indonesia.
Daniel              en_GB    # Hello, my name is Daniel. I am a British-English voice.
Diego               es_AR    # Hola, me llamo Diego y soy una voz española.
Ellen               nl_BE    # Hallo, mijn naam is Ellen. Ik ben een Belgische stem.
Fiona               en-scotland # Hello, my name is Fiona. I am a Scottish-English voice.
Fred                en_US    # I sure like being inside this fancy computer
Ioana               ro_RO    # Bună, mă cheamă Ioana . Sunt o voce românească.
Joana               pt_PT    # Olá, chamo-me Joana e dou voz ao português falado em Portugal.
Jorge               es_ES    # Hola, me llamo Jorge y soy una voz española.
Juan                es_MX    # Hola, me llamo Juan y soy una voz mexicana.
Kanya               th_TH    # สวัสดีค่ะ ดิฉันชื่อKanya
Karen               en_AU    # Hello, my name is Karen. I am an Australian-English voice.
Kyoko               ja_JP    # こんにちは、私の名前はKyokoです。日本語の音声をお届けします。
Laura               sk_SK    # Ahoj. Volám sa Laura . Som hlas v slovenskom jazyku.
Lekha               hi_IN    # नमस्कार, मेरा नाम लेखा है. मैं हिन्दी में बोलने वाली आवाज़ हूँ.
Luca                it_IT    # Salve, mi chiamo Luca e sono una voce italiana.
Luciana             pt_BR    # Olá, o meu nome é Luciana e a minha voz corresponde ao português que é falado no Brasil
Maged               ar_SA    # مرحبًا اسمي Maged. أنا عربي من السعودية.
Mariska             hu_HU    # Üdvözlöm! Mariska vagyok. Én vagyok a magyar hang.
Mei-Jia             zh_TW    # 您好，我叫美佳。我說國語。
Melina              el_GR    # Γεια σας, ονομάζομαι Melina. Είμαι μια ελληνική φωνή.
Milena              ru_RU    # Здравствуйте, меня зовут Milena. Я – русский голос системы.
Moira               en_IE    # Hello, my name is Moira. I am an Irish-English voice.
Monica              es_ES    # Hola, me llamo Monica y soy una voz española.
Nora                nb_NO    # Hei, jeg heter Nora. Jeg er en norsk stemme.
Paulina             es_MX    # Hola, me llamo Paulina y soy una voz mexicana.
Samantha            en_US    # Hello, my name is Samantha. I am an American-English voice.
Sara                da_DK    # Hej, jeg hedder Sara. Jeg er en dansk stemme.
Satu                fi_FI    # Hei, minun nimeni on Satu. Olen suomalainen ääni.
Sin-ji              zh_HK    # 您好，我叫 Sin-ji。我講廣東話。
Tessa               en_ZA    # Hello, my name is Tessa. I am a South African-English voice.
Thomas              fr_FR    # Bonjour, je m’appelle Thomas. Je suis une voix française.
Ting-Ting           zh_CN    # 您好，我叫Ting-Ting。我讲中文普通话。
Veena               en_IN    # Hello, my name is Veena. I am an Indian-English voice.
Victoria            en_US    # Isn't it nice to have a computer that will talk to you?
Xander              nl_NL    # Hallo, mijn naam is Xander. Ik ben een Nederlandse stem.
Yelda               tr_TR    # Merhaba, benim adım Yelda. Ben Türkçe bir sesim.
Yuna                ko_KR    # 안녕하세요. 제 이름은 Yuna입니다. 저는 한국어 음성입니다.
Yuri                ru_RU    # Здравствуйте, меня зовут Yuri. Я – русский голос системы.
Zosia               pl_PL    # Witaj. Mam na imię Zosia, jestem głosem kobiecym dla języka polskiego.
Zuzana              cs_CZ    # Dobrý den, jmenuji se Zuzana. Jsem český hlas."""

#time.sleep(4)

def test():
	print("jjj")

#speechSynthesizer.setDelegate(test)

print(speechSynthesizer.rate())
print(speechSynthesizer.volume())
print(speechSynthesizer.voice())

while speechSynthesizer.isSpeaking():
	pass
#from os import system
#system('say Hello world!')




['CAMLType', 'CAMLTypeForKey_', 'CA_addValue_multipliedBy_', 'CA_copyNumericValue_', 'CA_copyRenderValue', 'CA_distanceToValue_', 'CA_interpolateValue_byFraction_', 'CA_interpolateValues___interpolator_', 'CA_prepareRenderValue', 'CA_roundToIntegerFromValue_', 'NS_addTiledLayerDescendent_', 'NS_removeTiledLayerDescendent_', 'NS_tiledLayerVisibleRect', '___tryRetain_OA', '__autorelease_OA', '__dealloc_zombie', '__doc__', '__module__', '__pyobjc_PythonObject__', '__pyobjc_PythonTransient___', '__release_OA', '__retain_OA', '__slots__', '_accessibilityArrayAttributeCount_clientError_', '_accessibilityArrayAttributeValues_index_maxCount_clientError_', '_accessibilityAttributeNamesClientError_', '_accessibilityCanSetValueForAttribute_clientError_', '_accessibilityChildUIElementForSpecifierComponent_', '_accessibilityIndexOfChild_clientError_', '_accessibilityIsTableViewDescendant', '_accessibilitySetOverrideValue_forAttribute_', '_accessibilitySetUseConvenienceAPI_', '_accessibilitySpecifierComponentForChildUIElement_registerIfNeeded_', '_accessibilityUIElementSpecifier', '_accessibilityUIElementSpecifierForChild_registerIfNeeded_', '_accessibilityUIElementSpecifierRegisterIfNeeded_', '_accessibilityUseConvenienceAPI', '_accessibilityValueForAttribute_clientError_', '_addObserver_forProperty_options_context_', '_addOptionValue_toArray_withKey_type_', '_addPlaceholderOptionValue_isDefault_toArray_withKey_binder_binding_', '_allowsDirectEncoding', '_asScriptTerminologyNameArray', '_asScriptTerminologyNameString', '_beginSpeakingString_optionallyToURL_', '_bind_toController_withKeyPath_valueTransformerName_options_existingNibConnectors_connectorsToRemove_connectorsToAdd_', '_binderClassForBinding_withBinders_', '_binderForBinding_withBinders_createAutoreleasedInstanceIfNotFound_', '_binderWithClass_withBinders_createAutoreleasedInstanceIfNotFound_', '_bindingAdaptor', '_bindingInformationWithExistingNibConnectors_availableControllerChoices_', '_cfTypeID', '_changeValueForKey_key_key_usingBlock_', '_changeValueForKey_usingBlock_', '_changeValueForKeys_count_maybeOldValuesDict_maybeNewValuesDict_usingBlock_', '_cleanupBindingsWithExistingNibConnectors_exception_', '_compatibility_takeValue_forKey_', '_conformsToProtocolNamed_', '_continueSpeaking', '_copyDescription', '_createKeyValueBindingForKey_name_bindingType_', '_destroyObserverList', '_didChangeValuesForKeys_', '_didEndKeyValueObserving', '_feedbackWindowIsVisible', '_handleDefaultVoiceChange', '_handleErrorCallbackWithParams_', '_handlePhonemeCallbackWithOpcode_', '_handleSpeechDoneCallback', '_handleSyncCallbackWithMessage_', '_handleWordCallbackWithParams_', '_implicitObservationInfo', '_invokeSelector_withArguments_onKeyPath_', '_isAXConnector', '_isAccessibilityCandidateForSection_', '_isAccessibilityContainerSectionCandidate', '_isAccessibilityContentNavigatorSectionCandidate', '_isAccessibilityContentSectionCandidate', '_isAccessibilityTopLevelNavigatorSectionCandidate', '_isDeallocating', '_isKVOA', '_isToManyChangeInformation', '_localClassNameForClass', '_normalSpeakingRate', '_notifyObserversForKeyPath_change_', '_notifyObserversOfChangeFromValuesForKeys_toValuesForKeys_', '_objectForProperty_usingDataSize_withRequestedObjectClass_', '_observerStorage', '_observerStorageOfSize_', '_oldValueForKeyPath_', '_oldValueForKey_', '_optionDescriptionsForBinding_', '_overrideUseFastBlockObservers', '_pauseSpeakingAtBoundary_', '_pendingChangeNotificationsArrayForKey_create_', '_pitchBase', '_placeSuggestionsInDictionary_acceptableControllers_boundBinders_binder_binding_', '_pyobjc_performOnThreadWithResult_', '_pyobjc_performOnThread_', '_rate', '_receiveBox_', '_releaseBindingAdaptor', '_removeObserver_forProperty_', '_scriptingAddObjectsFromArray_toValueForKey_', '_scriptingAddObjectsFromSet_toValueForKey_', '_scriptingAddToReceiversArray_', '_scriptingAlternativeValueRankWithDescriptor_', '_scriptingArrayOfObjectsForSpecifier_', '_scriptingCanAddObjectsToValueForKey_', '_scriptingCanHandleCommand_', '_scriptingCanInsertBeforeOrReplaceObjectsAtIndexes_inValueForKey_', '_scriptingCanSetValue_forSpecifier_', '_scriptingCoerceValue_forKey_', '_scriptingCopyWithProperties_forValueForKey_ofContainer_', '_scriptingCount', '_scriptingCountNonrecursively', '_scriptingCountOfValueForKey_', '_scriptingDebugDescription', '_scriptingDescriptorOfComplexType_orReasonWhyNot_', '_scriptingDescriptorOfEnumeratorType_orReasonWhyNot_', '_scriptingDescriptorOfObjectType_orReasonWhyNot_', '_scriptingDescriptorOfValueType_orReasonWhyNot_', '_scriptingExists', '_scriptingIndexOfObjectForSpecifier_', '_scriptingIndexOfObjectWithName_inValueForKey_', '_scriptingIndexOfObjectWithUniqueID_inValueForKey_', '_scriptingIndexesOfObjectsForSpecifier_', '_scriptingIndicesOfObjectsAfterValidatingSpecifier_', '_scriptingIndicesOfObjectsForSpecifier_count_', '_scriptingInsertObject_inValueForKey_', '_scriptingInsertObjects_atIndexes_inValueForKey_', '_scriptingMightHandleCommand_', '_scriptingObjectAtIndex_inValueForKey_', '_scriptingObjectCountInValueForKey_', '_scriptingObjectForSpecifier_', '_scriptingObjectWithName_inValueForKey_', '_scriptingObjectWithUniqueID_inValueForKey_', '_scriptingObjectsAtIndexes_inValueForKey_', '_scriptingRemoveAllObjectsFromValueForKey_', '_scriptingRemoveObjectsAtIndexes_fromValueForKey_', '_scriptingRemoveValueForSpecifier_', '_scriptingReplaceObjectAtIndex_withObjects_inValueForKey_', '_scriptingSetOfObjectsForSpecifier_', '_scriptingSetValue_forKey_', '_scriptingSetValue_forSpecifier_', '_scriptingShouldCheckObjectIndexes', '_scriptingValueForKey_', '_scriptingValueForSpecifier_', '_setBindingAdaptor_', '_setObject_forBothSidesOfRelationshipWithKey_', '_setObject_forProperty_usingDataSize_', '_setPitchBase_', '_setRate_', '_setVolume_', '_setupCallbacks', '_shouldSearchChildrenForSection', '_stopSpeakingAtBoundary_', '_suggestedControllerKeyForController_binding_', '_supportsGetValueWithNameForKey_perhapsByOverridingClass_', '_supportsGetValueWithUniqueIDForKey_perhapsByOverridingClass_', '_tryRetain', '_unbind_existingNibConnectors_connectorsToRemove_connectorsToAdd_', '_volume', '_willBeginKeyValueObserving', '_willChangeValuesForKeys_', 'accessibilityAddTemporaryChild_', 'accessibilityAllowsOverriddenAttributesWhenIgnored', 'accessibilityArrayAttributeCount_', 'accessibilityArrayAttributeValues_index_maxCount_', 'accessibilityAttributeValue_forParameter_', 'accessibilityAttributedValueForStringAttributeAttributeForParameter_', 'accessibilityDecodeOverriddenAttributes_', 'accessibilityEncodeOverriddenAttributes_', 'accessibilityIndexForChildUIElementAttributeForParameter_', 'accessibilityIndexOfChild_', 'accessibilityOverriddenAttributes', 'accessibilityParameterizedAttributeNames', 'accessibilityPerformShowMenuOfChild_', 'accessibilityPresenterProcessIdentifier', 'accessibilityRemoveTemporaryChild_', 'accessibilityReplaceRange_withText_', 'accessibilitySetOverrideValue_forAttribute_', 'accessibilitySetPresenterProcessIdentifier_', 'accessibilityShouldSendNotification_', 'accessibilityShouldUseUniqueId', 'accessibilitySupportsNotifications', 'accessibilitySupportsOverriddenAttributes', 'accessibilityTemporaryChildren', 'accessibilityVisibleArea', 'addChainedObservers_', 'addObject_toBothSidesOfRelationshipWithKey_', 'addObject_toPropertyWithKey_', 'addObservationTransformer_', 'addObserverBlock_', 'addObserver_', 'addObserver_forKeyPath_options_context_', 'addObserver_forObservableKeyPath_', 'addSpeechDictionary_', 'allPropertyKeys', 'allowsWeakReference', 'attributeKeys', 'autoContentAccessingProxy', 'autorelease', 'awakeAfterUsingCoder_', 'awakeFromNib', 'bind_toObject_withKeyPath_options_', 'boolValueSafe', 'boolValueSafe_', 'bs_encoded', 'bs_isPlistableType', 'bs_secureEncoded', 'classCode', 'classDescription', 'classDescriptionForDestinationKey_', 'classForArchiver', 'classForCoder', 'classForKeyedArchiver', 'classForPortCoder', 'className', 'class__', 'clearProperties', 'coerceValueForScriptingProperties_', 'coerceValue_forKey_', 'conformsToProtocol_', 'continueSpeaking', 'copy', 'copyScriptingValue_forKey_withProperties_', 'createKeyValueBindingForKey_typeMask_', 'dealloc', 'dealloc', 'debugDescription', 'delegate', 'description', 'description', 'dictionaryWithValuesForKeys_', 'didChangeValueForKey_', 'didChangeValueForKey_withSetMutation_usingObjects_', 'didChange_valuesAtIndexes_forKey_', 'doesContain_', 'doesNotRecognizeSelector_', 'doesNotRecognizeSelector_', 'doubleValueSafe', 'doubleValueSafe_', 'encodeWithCAMLWriter_', 'entityName', 'exposedBindings', 'finalize', 'finishObserving', 'flushKeyBindings', 'forwardInvocation_', 'forwardingTargetForSelector_', 'handleQueryWithUnboundKey_', 'handleTakeValue_forUnboundKey_', 'hash', 'implementsSelector_', 'infoForBinding_', 'init', 'init', 'initWithVoice_', 'initWithVoice_', 'insertValue_atIndex_inPropertyWithKey_', 'insertValue_inPropertyWithKey_', 'int64ValueSafe', 'int64ValueSafe_', 'inverseForRelationshipKey_', 'isCaseInsensitiveLike_', 'isEqualTo_', 'isEqual_', 'isFault', 'isGreaterThanOrEqualTo_', 'isGreaterThan_', 'isKindOfClass_', 'isLessThanOrEqualTo_', 'isLessThan_', 'isLike_', 'isMemberOfClass_', 'isNSArray__', 'isNSCFConstantString__', 'isNSData__', 'isNSDate__', 'isNSDictionary__', 'isNSNumber__', 'isNSObject__', 'isNSOrderedSet__', 'isNSSet__', 'isNSString__', 'isNSTimeZone__', 'isNSValue__', 'isNotEqualTo_', 'isProxy', 'isSpeaking', 'isToManyKey_', 'keyValueBindingForKey_typeMask_', 'methodDescriptionForSelector_', 'methodForSelector_', 'methodSignatureForSelector_', 'methodSignatureForSelector_', 'mutableArrayValueForKeyPath_', 'mutableArrayValueForKey_', 'mutableCopy', 'mutableOrderedSetValueForKeyPath_', 'mutableOrderedSetValueForKey_', 'mutableSetValueForKeyPath_', 'mutableSetValueForKey_', 'newScriptingObjectOfClass_forValueForKey_withContentsValue_properties_', 'objectForProperty_error_', 'objectSpecifier', 'observationInfo', 'observeValueForKeyPath_ofObject_change_context_', 'optionDescriptionsForBinding_', 'ownsDestinationObjectsForRelationshipKey_', 'pauseSpeakingAtBoundary_', 'performSelectorInBackground_withObject_', 'performSelectorOnMainThread_withObject_waitUntilDone_', 'performSelectorOnMainThread_withObject_waitUntilDone_modes_', 'performSelector_', 'performSelector_object_afterDelay_', 'performSelector_onThread_withObject_waitUntilDone_', 'performSelector_onThread_withObject_waitUntilDone_modes_', 'performSelector_withObject_', 'performSelector_withObject_afterDelay_', 'performSelector_withObject_afterDelay_inModes_', 'performSelector_withObject_withObject_', 'phonemesFromText_', 'prepareForInterfaceBuilder', 'pyobjc_performSelectorInBackground_withObject_', 'pyobjc_performSelectorOnMainThread_withObject_', 'pyobjc_performSelectorOnMainThread_withObject_modes_', 'pyobjc_performSelectorOnMainThread_withObject_waitUntilDone_', 'pyobjc_performSelectorOnMainThread_withObject_waitUntilDone_modes_', 'pyobjc_performSelector_onThread_withObject_', 'pyobjc_performSelector_onThread_withObject_modes_', 'pyobjc_performSelector_onThread_withObject_waitUntilDone_', 'pyobjc_performSelector_onThread_withObject_waitUntilDone_modes_', 'pyobjc_performSelector_withObject_afterDelay_', 'pyobjc_performSelector_withObject_afterDelay_inModes_', 'rate', 'receiveObservedError_', 'receiveObservedValue_', 'release', 'remoteInvocation_sessionManager_invocationHandler_', 'removeObject_fromBothSidesOfRelationshipWithKey_', 'removeObject_fromPropertyWithKey_', 'removeObservation_', 'removeObservation_forObservableKeyPath_', 'removeObserver_forKeyPath_', 'removeObserver_forKeyPath_context_', 'removeValueAtIndex_fromPropertyWithKey_', 'replaceValueAtIndex_inPropertyWithKey_withValue_', 'replacementObjectForArchiver_', 'replacementObjectForCoder_', 'replacementObjectForKeyedArchiver_', 'replacementObjectForPortCoder_', 'respondsToSelector_', 'retain', 'retainCount', 'retainWeakReference', 'scriptingProperties', 'scriptingValueForSpecifier_', 'self', 'setDelegate_', 'setNilValueForKey_', 'setObject_forProperty_error_', 'setObservationInfo_', 'setObservation_forObservingKeyPath_', 'setRate_', 'setScriptingProperties_', 'setUserInterfaceItemIdentifier_', 'setUsesFeedbackWindow_', 'setValue_forKeyPath_', 'setValue_forKey_', 'setValue_forUndefinedKey_', 'setValuesForKeysWithDictionary_', 'setVoice_', 'setVolume_', 'startSpeakingString_', 'startSpeakingString_', 'startSpeakingString_toURL_', 'stopSpeaking', 'stopSpeakingAtBoundary_', 'storedValueForKey_', 'stringValueSafe', 'stringValueSafe_', 'superclass', 'takeStoredValue_forKey_', 'takeStoredValuesFromDictionary_', 'takeValue_forKeyPath_', 'takeValue_forKey_', 'takeValuesFromDictionary_', 'toManyRelationshipKeys', 'toOneRelationshipKeys', 'unableToSetNilForKey_', 'unbind_', 'userInterfaceItemIdentifier', 'usesFeedbackWindow', 'utf8ValueSafe', 'utf8ValueSafe_', 'validateTakeValue_forKeyPath_', 'validateValue_forKeyPath_error_', 'validateValue_forKey_', 'validateValue_forKey_error_', 'valueAtIndex_inPropertyWithKey_', 'valueClassForBinding_', 'valueForKeyPath_', 'valueForKey_', 'valueForUndefinedKey_', 'valueWithName_inPropertyWithKey_', 'valueWithUniqueID_inPropertyWithKey_', 'valuesForKeys_', 'voice', 'volume', 'willChangeValueForKey_', 'willChangeValueForKey_withSetMutation_usingObjects_', 'willChange_valuesAtIndexes_forKey_', 'zone']