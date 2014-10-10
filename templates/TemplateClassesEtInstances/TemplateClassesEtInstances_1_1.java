package com.modeliosoft.templates;

import java.util.List;
import java.util.ArrayList;
import java.util.Calendar;
import java.io.IOException;
import java.io.InputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.modelio.metamodel.*;
import org.modelio.metamodel.analyst.*;
import org.modelio.metamodel.bpmn.processCollaboration.*;
import org.modelio.metamodel.bpmn.rootElements.*;
import org.modelio.metamodel.bpmn.flows.*;
import org.modelio.metamodel.bpmn.activities.*;
import org.modelio.metamodel.bpmn.events.*;
import org.modelio.metamodel.bpmn.gateways.*;
import org.modelio.metamodel.bpmn.objects.*;
import org.modelio.metamodel.bpmn.resources.*;
import org.modelio.metamodel.bpmn.bpmnDiagrams.*;
import org.modelio.metamodel.bpmn.bpmnService.*;
import org.modelio.metamodel.diagrams.*;
import org.modelio.metamodel.mda.*;
import org.modelio.metamodel.uml.infrastructure.*;
import org.modelio.metamodel.uml.infrastructure.matrix.*;
import org.modelio.metamodel.uml.infrastructure.properties.*;
import org.modelio.metamodel.uml.statik.*;
import org.modelio.metamodel.uml.statik.Package;
import org.modelio.metamodel.uml.statik.Interface;
import org.modelio.metamodel.uml.statik.Class;
import org.modelio.metamodel.uml.behavior.activityModel.*;
import org.modelio.metamodel.uml.behavior.commonBehaviors.*;
import org.modelio.metamodel.uml.behavior.interactionModel.*;
import org.modelio.metamodel.uml.behavior.stateMachineModel.*;
import org.modelio.metamodel.uml.behavior.usecaseModel.*;
import org.modelio.metamodel.uml.behavior.communicationModel.*;
import org.modelio.metamodel.uml.informationFlow.*;
import org.modelio.metamodel.visitors.*;
import org.modelio.vcore.smkernel.mapi.MObject;
import com.modelio.module.documentpublisher.impl.DocumentPublisherLogService;
import com.modelio.module.documentpublisher.impl.DocumentPublisherModule;
import com.modelio.module.documentpublisher.nodes.NodeManager;
import com.modelio.module.documentpublisher.nodes.model.*;
import com.modelio.module.documentpublisher.nodes.other.RootNode.RootBehavior;
import com.modelio.module.documentpublisher.nodes.template.generator.FormatNotImplementedException;
import com.modelio.module.documentpublisher.nodes.template.TemplateNodeException;
import com.modelio.module.documentpublisher.nodes.template.ITemplate;
import com.modelio.module.documentpublisher.nodes.template.context.Revision;
import com.modelio.module.documentpublisher.nodes.template.context.TemplateParameter;
import com.modelio.module.documentpublisher.nodes.template.context.ActivationContext;
import com.modelio.module.documentpublisher.nodes.template.context.IterationContext;
import com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType;
import com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType;
import com.modelio.module.documentpublisher.nodes.other.ProcedureNode.ProcedureType;
import com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType;
import com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType;
import com.modelio.module.documentpublisher.nodes.other.NodeCallNode.NodeCallType;
import com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType;
import com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType;
import com.modelio.module.documentpublisher.nodes.production.TableNode.TableType;
import com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType;
import com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType;
import com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType;
import com.modelio.module.documentpublisher.nodes.other.DummyNode.DummyNodeType;
import com.modelio.module.documentpublisher.nodes.other.RootNode.RootType;
import com.modelio.module.documentpublisher.nodes.navigation.JythonNode.JythonType;

public class TemplateClassesEtInstances_1_1 implements ITemplate {

private void loadAllNodes() {
  NodeManager nodeManager = NodeManager.getInstance ();
List<INodeType> controls = new ArrayList<> ();
controls.add (new com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.ProcedureNode.ProcedureType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.NodeCallNode.NodeCallType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.TableNode.TableType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.DummyNode.DummyNodeType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.RootNode.RootType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.JythonNode.JythonType ());
for (INodeType nodeType : controls) {
    NodeInstance instance = new NodeInstance (nodeType);
    nodeManager.registerNode (instance);
}
}

protected void filterNodoc(List<? extends MObject> list) {
   for (MObject e : new ArrayList<>(list)) {
        if (e instanceof ModelElement && ((ModelElement) e).isTagged("ModelerModule", "nodoc")) {
            list.remove(e);
        }
    }
}

private void initJythonMacros() {
   try {
      String macros = loadMacroFile();
      if (macros != null && !macros.isEmpty()) {
         this.activationContext.getJythonEngine().eval(macros);
      }
   } catch (Exception e) {
      // Consider there is no macro file to load.
   }
}

private String loadMacroFile() throws IOException {
    InputStream resourceAsStream = this.getClass().getResourceAsStream("/macros.py");
    if (resourceAsStream != null) {
        StringBuilder script = new StringBuilder();
        try (BufferedReader r = new BufferedReader(new InputStreamReader(resourceAsStream))) {
           String l;
           while((l = r.readLine()) != null) {
               script.append(l);
               script.append("\n");
           }
           r.close();
        }
        return script.toString();
    }
    return null;
}

private final ActivationContext activationContext;
private final DocumentPublisherLogService logger;

public TemplateClassesEtInstances_1_1() {
  loadAllNodes();
  this.logger = DocumentPublisherModule.logService;
  this.activationContext = new ActivationContext();

  this.activationContext.addParameter(new TemplateParameter("Title", "Document title", "Document"));
  this.activationContext.addParameter(new TemplateParameter("Subject", "Document subject", "Subject"));
  this.activationContext.addParameter(new TemplateParameter("Category", "Document category", "Category"));
  this.activationContext.addParameter(new TemplateParameter("Status", "Document status", "Draft"));
  this.activationContext.addParameter(new TemplateParameter("Author", "Document author", "DocumentPublisher"));
  this.activationContext.addParameter(new TemplateParameter("Version", "Document version", "1.0"));
  this.activationContext.addParameter(new TemplateParameter("Company", "Document company", "Modeliosoft"));
  this.activationContext.addParameter(new TemplateParameter("Address", "Document address", ""));
  this.activationContext.addParameter(new TemplateParameter("Copyright", "Document copyright", ""));
  this.activationContext.addParameter(new TemplateParameter("TOC Depth", "Maximum depth of the table of contents", "3"));
}

@Override
public ActivationContext getActivationContext() {
    return this.activationContext;
}

@Override
public TemplateParameter getParameter(String name) {
    return this.activationContext.getParameter(name);
}

@Override
public List<TemplateParameter> getParameters() {
    return this.activationContext.getParameters();
}

@Override
public String getTemplateDescription() {
String description = "";
description += "";
    return description;
}

@Override
public String getTemplateName() {
    return "TemplateClassesEtInstances_1_1";
}

public boolean activate(String baseFile, String targetFile, List<ModelElement>l1, GenerationMode mode, Target target, int titleLevel, List<DocumentContent> docContent, List<Revision> revisions) throws TemplateNodeException, FormatNotImplementedException {
logger.info("TemplateClassesEtInstances_1_1 activated at " + Calendar.getInstance().getTime());
initJythonMacros();

try {
activationContext.setTargetFormat(target);
activationContext.setMode(mode);
activationContext.setDocumentContent(docContent);
activationContext.setRevisions(revisions);
NodeInstance n1 = new NodeInstance();
n1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.other.RootNode.RootType");
n1.setContext (activationContext);
n1.setParameter ("releaseNotes", "");
n1.setParameter ("creationDate", "Wed Apr 02 18:24:35 CEST 2014");
n1.setParameter ("description", "");
n1.setParameter ("templateparameters", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAKdwQAAAAK\r\nc3IATWNvbS5tb2RlbGlvLm1vZHVsZS5kb2N1bWVudHB1Ymxpc2hlci5ub2Rlcy50ZW1wbGF0ZS5j\r\nb250ZXh0LlRlbXBsYXRlUGFyYW1ldGVyIihydAjuqx0CAAVaAAtwcm9wYWdhdGlvbkwADGRlZmF1\r\nbHRWYWx1ZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAC2Rlc2NyaXB0aW9ucQB+AANMAA5lZmZlY3Rp\r\ndmVWYWx1ZXEAfgADTAAEbmFtZXEAfgADeHABdAAIRG9jdW1lbnR0AA5Eb2N1bWVudCB0aXRsZXQA\r\nAHQABVRpdGxlc3EAfgACAXQAB1N1YmplY3R0ABBEb2N1bWVudCBzdWJqZWN0cQB+AAdxAH4ACnNx\r\nAH4AAgF0AAhDYXRlZ29yeXQAEURvY3VtZW50IGNhdGVnb3J5cQB+AAdxAH4ADXNxAH4AAgF0AAVE\r\ncmFmdHQAD0RvY3VtZW50IHN0YXR1c3EAfgAHdAAGU3RhdHVzc3EAfgACAXQAEURvY3VtZW50UHVi\r\nbGlzaGVydAAPRG9jdW1lbnQgYXV0aG9ycQB+AAd0AAZBdXRob3JzcQB+AAIBdAADMS4wdAAQRG9j\r\ndW1lbnQgdmVyc2lvbnEAfgAHdAAHVmVyc2lvbnNxAH4AAgF0AAtNb2RlbGlvc29mdHQAEERvY3Vt\r\nZW50IGNvbXBhbnlxAH4AB3QAB0NvbXBhbnlzcQB+AAIBcQB+AAd0ABBEb2N1bWVudCBhZGRyZXNz\r\ncQB+AAd0AAdBZGRyZXNzc3EAfgACAXEAfgAHdAASRG9jdW1lbnQgY29weXJpZ2h0cQB+AAd0AAlD\r\nb3B5cmlnaHRzcQB+AAIBdAABM3QAJk1heGltdW0gZGVwdGggb2YgdGhlIHRhYmxlIG9mIGNvbnRl\r\nbnRzcQB+AAd0AAlUT0MgRGVwdGh4");
n1.setParameter ("modificationDate", "Wed Apr 02 22:15:12 CEST 2014");
n1.setParameter ("baseFile", "");
n1.setParameter ("targetFile", "");
n1.setParameter ("version", "1.1");
n1.setParameter("targetFile", targetFile);
n1.setParameter("baseFile", baseFile);
int maxIndex = l1.size();
RootBehavior rb = ((RootBehavior)n1.getNodeType ().getNodeBehavior ());
for (int index = 0; index < maxIndex; index++) {
IterationContext iterationContext = new IterationContext(l1.get(index));
MObject elt = l1.get(index);
iterationContext.setParameter("titleLevel", titleLevel);
rb.beginProduction(n1, elt, index, maxIndex, iterationContext);
m1(elt, index, maxIndex, iterationContext);
//m2(elt, index, maxIndex, iterationContext);
//m3(elt, index, maxIndex, iterationContext);
//m4(elt, index, maxIndex, iterationContext);
//m5(elt, index, maxIndex, iterationContext);
//m6(elt, index, maxIndex, iterationContext);
//m7(elt, index, maxIndex, iterationContext);
}
if (rb.endProduction(n1, null)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
logger.info("TemplateClassesEtInstances_1_1 completed at" + Calendar.getInstance().getTime());
return true;
}


/* RootType - 1 - TemplateClassesEtInstances_1_1 */
private void m1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m1_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 1*/


/* SectionType - 1_1 - MainSection */
private void m1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_1 = new NodeInstance();
n1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n1_1.setContext (activationContext);
n1_1.setParameter ("startOnNewPage", false);
n1_1.setParameter ("text", "$Name");
n1_1.setParameter ("removeEmptySection", true);
n1_1.setParameter ("sectionStyle", "Titre n");
n1_1.setParameter ("numbering", true);
n1_1.setParameter ("showIcon", false);
n1_1.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n1_1, elt, index, maxIndex, iterationContext);
m2(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 1_1*/


/* ProcedureType - 2 - PackageContent */
private void m2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m3(elt, index, maxIndex, iterationContext);
m4(elt, index, maxIndex, iterationContext);
m5(elt, index, maxIndex, iterationContext);
m6(elt, index, maxIndex, iterationContext);
m7(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 2*/


/* ProcedureType - 3 - ClassifierTable */
private void m3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m3_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3*/


/* TableType - 3_1 - ClassifierTable */
private void m3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1 = new NodeInstance();
n3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableNode.TableType");
n3_1.setContext (activationContext);
n3_1.setParameter ("headerTitle19", "");
n3_1.setParameter ("headerTitle18", "");
n3_1.setParameter ("headerTitle17", "");
n3_1.setParameter ("headerTitle16", "");
n3_1.setParameter ("headerTitle39", "");
n3_1.setParameter ("headerTitle38", "");
n3_1.setParameter ("headerTitle36", "");
n3_1.setParameter ("headerTitle10", "");
n3_1.setParameter ("headerTitle37", "");
n3_1.setParameter ("headerTitle11", "");
n3_1.setParameter ("headerTitle34", "");
n3_1.setParameter ("headerTitle35", "");
n3_1.setParameter ("headerTitle32", "");
n3_1.setParameter ("headerTitle14", "");
n3_1.setParameter ("headerTitle33", "");
n3_1.setParameter ("headerTitle0", "Classe");
n3_1.setParameter ("tableWithHeader", true);
n3_1.setParameter ("headerTitle15", "");
n3_1.setParameter ("headerTitle30", "");
n3_1.setParameter ("headerTitle1", "Résumé");
n3_1.setParameter ("headerTitle12", "");
n3_1.setParameter ("headerTitle31", "");
n3_1.setParameter ("headerTitle2", "Instances");
n3_1.setParameter ("headerTitle13", "");
n3_1.setParameter ("headerTitle3", "");
n3_1.setParameter ("headerTitle4", "");
n3_1.setParameter ("headerAlignment", "CENTER");
n3_1.setParameter ("headerTitle5", "");
n3_1.setParameter ("headerTitle6", "");
n3_1.setParameter ("headerTitle7", "");
n3_1.setParameter ("headerTitle8", "");
n3_1.setParameter ("headerTitle9", "");
n3_1.setParameter ("headerTitle49", "");
n3_1.setParameter ("nbLines", 3);
n3_1.setParameter ("tableStyle", "ListeclaireAccent1");
n3_1.setParameter ("caption", "");
n3_1.setParameter ("headerTitle28", "");
n3_1.setParameter ("headerTitle27", "");
n3_1.setParameter ("headerTitle29", "");
n3_1.setParameter ("headerTitle23", "");
n3_1.setParameter ("headerTitle24", "");
n3_1.setParameter ("headerTitle25", "");
n3_1.setParameter ("headerTitle26", "");
n3_1.setParameter ("headerTitle20", "");
n3_1.setParameter ("headerTitle40", "");
n3_1.setParameter ("headerTitle21", "");
n3_1.setParameter ("horizontal", true);
n3_1.setParameter ("headerTitle22", "");
n3_1.setParameter ("tableAlignment", "BOTH");
n3_1.setParameter ("headerTitle42", "");
n3_1.setParameter ("headerTitle41", "");
n3_1.setParameter ("headerTitle44", "");
n3_1.setParameter ("headerTitle43", "");
n3_1.setParameter ("headerTitle46", "");
n3_1.setParameter ("headerTitle45", "");
n3_1.setParameter ("headerTitle48", "");
n3_1.setParameter ("headerTitle47", "");
IProductionBehavior pb = ((IProductionBehavior)n3_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1, elt, index, maxIndex, iterationContext);
m3_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1*/


/* SmartNavigationType - 3_1_1 - Classifiers */
private void m3_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1 = new NodeInstance();
n3_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n3_1_1.setContext (activationContext);
n3_1_1.setInputMetaclass(Package.class);
n3_1_1.setOutputMetaclass(Classifier.class);
n3_1_1.setParameter ("sort", false);
n3_1_1.setParameter ("outputStereotype", "None");
n3_1_1.setParameter ("relation", "OwnedElement");
n3_1_1.setParameter ("sequenceMode", true);
n3_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n3_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l3_1_1 = nb.navigate(n3_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l3_1_1);
for (int i3_1_1 = 0; i3_1_1 < l3_1_1.size(); i3_1_1++) {
iterationContext.addContext(new IterationContext(l3_1_1.get(i3_1_1)));
MObject e3_1_1 = l3_1_1.get(i3_1_1);
m3_1_1_1(e3_1_1, i3_1_1, l3_1_1.size(), iterationContext);
m3_1_1_2(e3_1_1, i3_1_1, l3_1_1.size(), iterationContext);
m3_1_1_3(e3_1_1, i3_1_1, l3_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1*/


/* TableCellType - 3_1_1_1 - ClassifierStereotypeAndNameCell */
private void m3_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_1 = new NodeInstance();
n3_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n3_1_1_1.setContext (activationContext);
n3_1_1_1.setParameter ("insertionEnabled", true);
n3_1_1_1.setParameter ("alignment", "LEFT");
n3_1_1_1.setParameter ("text", "");
n3_1_1_1.setParameter ("paragraphStyle", "Normal");
n3_1_1_1.setParameter ("characterStyle", "None");
n3_1_1_1.setParameter ("columnIndex", 0);
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_1, elt, index, maxIndex, iterationContext);
m3_1_1_1_1(elt, index, maxIndex, iterationContext);
m3_1_1_1_2(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_1*/


/* SmartNavigationType - 3_1_1_1_1 - Stereotypes */
private void m3_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_1_1 = new NodeInstance();
n3_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n3_1_1_1_1.setContext (activationContext);
n3_1_1_1_1.setInputMetaclass(Class.class);
n3_1_1_1_1.setOutputMetaclass(Stereotype.class);
n3_1_1_1_1.setParameter ("sort", false);
n3_1_1_1_1.setParameter ("outputStereotype", "None");
n3_1_1_1_1.setParameter ("relation", "Extension");
n3_1_1_1_1.setParameter ("sequenceMode", true);
n3_1_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n3_1_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l3_1_1_1_1 = nb.navigate(n3_1_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l3_1_1_1_1);
for (int i3_1_1_1_1 = 0; i3_1_1_1_1 < l3_1_1_1_1.size(); i3_1_1_1_1++) {
iterationContext.addContext(new IterationContext(l3_1_1_1_1.get(i3_1_1_1_1)));
MObject e3_1_1_1_1 = l3_1_1_1_1.get(i3_1_1_1_1);
m3_1_1_1_1_1(e3_1_1_1_1, i3_1_1_1_1, l3_1_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_1_1*/


/* CommaSeparatedListType - 3_1_1_1_1_1 - <<,>> */
private void m3_1_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_1_1_1 = new NodeInstance();
n3_1_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n3_1_1_1_1_1.setContext (activationContext);
n3_1_1_1_1_1.setParameter ("text", "");
n3_1_1_1_1_1.setParameter ("startSeparator", "<<");
n3_1_1_1_1_1.setParameter ("characterStyle", "None");
n3_1_1_1_1_1.setParameter ("separator", ",");
n3_1_1_1_1_1.setParameter ("endSeparator", ">> ");
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_1_1_1, elt, index, maxIndex, iterationContext);
m3_1_1_1_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_1_1_1*/


/* CharacterType - 3_1_1_1_1_1_1 - StereotypeName */
private void m3_1_1_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_1_1_1_1 = new NodeInstance();
n3_1_1_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n3_1_1_1_1_1_1.setContext (activationContext);
n3_1_1_1_1_1_1.setParameter ("text", "$Name");
n3_1_1_1_1_1_1.setParameter ("characterStyle", "None");
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_1_1_1_1*/


/* CharacterType - 3_1_1_1_2 - ClassName */
private void m3_1_1_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_1_2 = new NodeInstance();
n3_1_1_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n3_1_1_1_2.setContext (activationContext);
n3_1_1_1_2.setParameter ("text", "$Name");
n3_1_1_1_2.setParameter ("characterStyle", "None");
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_1_2.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_1_2, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_1_2, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_1_2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_1_2*/


/* NoteNavigationType - 3_1_1_2 - Summary */
private void m3_1_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_2 = new NodeInstance();
n3_1_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n3_1_1_2.setContext (activationContext);
n3_1_1_2.setInputMetaclass(Class.class);
n3_1_1_2.setOutputMetaclass(Note.class);
n3_1_1_2.setParameter ("noteName", "summary");
n3_1_1_2.setParameter ("sort", false);
n3_1_1_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n3_1_1_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l3_1_1_2 = nb.navigate(n3_1_1_2, elt, index, maxIndex, iterationContext);
filterNodoc(l3_1_1_2);
for (int i3_1_1_2 = 0; i3_1_1_2 < l3_1_1_2.size(); i3_1_1_2++) {
iterationContext.addContext(new IterationContext(l3_1_1_2.get(i3_1_1_2)));
MObject e3_1_1_2 = l3_1_1_2.get(i3_1_1_2);
m3_1_1_2_1(e3_1_1_2, i3_1_1_2, l3_1_1_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_2*/


/* TableCellType - 3_1_1_2_1 - SummaryCell */
private void m3_1_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_2_1 = new NodeInstance();
n3_1_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n3_1_1_2_1.setContext (activationContext);
n3_1_1_2_1.setParameter ("insertionEnabled", true);
n3_1_1_2_1.setParameter ("alignment", "LEFT");
n3_1_1_2_1.setParameter ("text", "$Name");
n3_1_1_2_1.setParameter ("paragraphStyle", "Normal");
n3_1_1_2_1.setParameter ("characterStyle", "None");
n3_1_1_2_1.setParameter ("columnIndex", 1);
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_2_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_2_1*/


/* TableCellType - 3_1_1_3 - InstanceNamesCell */
private void m3_1_1_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_3 = new NodeInstance();
n3_1_1_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n3_1_1_3.setContext (activationContext);
n3_1_1_3.setParameter ("insertionEnabled", false);
n3_1_1_3.setParameter ("alignment", "LEFT");
n3_1_1_3.setParameter ("text", "$Name");
n3_1_1_3.setParameter ("paragraphStyle", "Normal");
n3_1_1_3.setParameter ("characterStyle", "None");
n3_1_1_3.setParameter ("columnIndex", 2);
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_3, elt, index, maxIndex, iterationContext);
m3_1_1_3_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_3", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_3*/


/* SmartNavigationType - 3_1_1_3_1 - Instances */
private void m3_1_1_3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_3_1 = new NodeInstance();
n3_1_1_3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n3_1_1_3_1.setContext (activationContext);
n3_1_1_3_1.setInputMetaclass(Classifier.class);
n3_1_1_3_1.setOutputMetaclass(Instance.class);
n3_1_1_3_1.setParameter ("sort", false);
n3_1_1_3_1.setParameter ("outputStereotype", "None");
n3_1_1_3_1.setParameter ("relation", "Representing");
n3_1_1_3_1.setParameter ("sequenceMode", true);
n3_1_1_3_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n3_1_1_3_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l3_1_1_3_1 = nb.navigate(n3_1_1_3_1, elt, index, maxIndex, iterationContext);
filterNodoc(l3_1_1_3_1);
for (int i3_1_1_3_1 = 0; i3_1_1_3_1 < l3_1_1_3_1.size(); i3_1_1_3_1++) {
iterationContext.addContext(new IterationContext(l3_1_1_3_1.get(i3_1_1_3_1)));
MObject e3_1_1_3_1 = l3_1_1_3_1.get(i3_1_1_3_1);
m3_1_1_3_1_1(e3_1_1_3_1, i3_1_1_3_1, l3_1_1_3_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_3_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_3_1*/


/* ParagraphType - 3_1_1_3_1_1 - InstanceName */
private void m3_1_1_3_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1_1_3_1_1 = new NodeInstance();
n3_1_1_3_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n3_1_1_3_1_1.setContext (activationContext);
n3_1_1_3_1_1.setParameter ("text", "$Name");
n3_1_1_3_1_1.setParameter ("paragraphStyle", "Paragraphedeliste");
n3_1_1_3_1_1.setParameter ("characterStyle", "None");
n3_1_1_3_1_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n3_1_1_3_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1_1_3_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1_1_3_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1_1_3_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 3_1_1_3_1_1*/


/* ProcedureType - 4 - InstanceTable */
private void m4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m4_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4*/


/* TableType - 4_1 - InstanceTable */
private void m4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1 = new NodeInstance();
n4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableNode.TableType");
n4_1.setContext (activationContext);
n4_1.setParameter ("headerTitle19", "");
n4_1.setParameter ("headerTitle18", "");
n4_1.setParameter ("headerTitle17", "");
n4_1.setParameter ("headerTitle16", "");
n4_1.setParameter ("headerTitle39", "");
n4_1.setParameter ("headerTitle38", "");
n4_1.setParameter ("headerTitle36", "");
n4_1.setParameter ("headerTitle10", "");
n4_1.setParameter ("headerTitle37", "");
n4_1.setParameter ("headerTitle11", "");
n4_1.setParameter ("headerTitle34", "");
n4_1.setParameter ("headerTitle35", "");
n4_1.setParameter ("headerTitle32", "");
n4_1.setParameter ("headerTitle14", "");
n4_1.setParameter ("headerTitle33", "");
n4_1.setParameter ("headerTitle0", "Instance");
n4_1.setParameter ("tableWithHeader", true);
n4_1.setParameter ("headerTitle15", "");
n4_1.setParameter ("headerTitle30", "");
n4_1.setParameter ("headerTitle1", "Description");
n4_1.setParameter ("headerTitle12", "");
n4_1.setParameter ("headerTitle31", "");
n4_1.setParameter ("headerTitle2", "Classe");
n4_1.setParameter ("headerTitle13", "");
n4_1.setParameter ("headerTitle3", "Scénarii");
n4_1.setParameter ("headerTitle4", "");
n4_1.setParameter ("headerAlignment", "CENTER");
n4_1.setParameter ("headerTitle5", "");
n4_1.setParameter ("headerTitle6", "");
n4_1.setParameter ("headerTitle7", "");
n4_1.setParameter ("headerTitle8", "");
n4_1.setParameter ("headerTitle9", "");
n4_1.setParameter ("headerTitle49", "");
n4_1.setParameter ("nbLines", 4);
n4_1.setParameter ("tableStyle", "ListeclaireAccent1");
n4_1.setParameter ("caption", "");
n4_1.setParameter ("headerTitle28", "");
n4_1.setParameter ("headerTitle27", "");
n4_1.setParameter ("headerTitle29", "");
n4_1.setParameter ("headerTitle23", "");
n4_1.setParameter ("headerTitle24", "");
n4_1.setParameter ("headerTitle25", "");
n4_1.setParameter ("headerTitle26", "");
n4_1.setParameter ("headerTitle20", "");
n4_1.setParameter ("headerTitle40", "");
n4_1.setParameter ("headerTitle21", "");
n4_1.setParameter ("horizontal", true);
n4_1.setParameter ("headerTitle22", "");
n4_1.setParameter ("tableAlignment", "BOTH");
n4_1.setParameter ("headerTitle42", "");
n4_1.setParameter ("headerTitle41", "");
n4_1.setParameter ("headerTitle44", "");
n4_1.setParameter ("headerTitle43", "");
n4_1.setParameter ("headerTitle46", "");
n4_1.setParameter ("headerTitle45", "");
n4_1.setParameter ("headerTitle48", "");
n4_1.setParameter ("headerTitle47", "");
IProductionBehavior pb = ((IProductionBehavior)n4_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1, elt, index, maxIndex, iterationContext);
m4_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1*/


/* SmartNavigationType - 4_1_1 - Instances */
private void m4_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1 = new NodeInstance();
n4_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1.setContext (activationContext);
n4_1_1.setInputMetaclass(Package.class);
n4_1_1.setOutputMetaclass(Instance.class);
n4_1_1.setParameter ("sort", false);
n4_1_1.setParameter ("outputStereotype", "None");
n4_1_1.setParameter ("relation", "Declared");
n4_1_1.setParameter ("sequenceMode", true);
n4_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1 = nb.navigate(n4_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1);
for (int i4_1_1 = 0; i4_1_1 < l4_1_1.size(); i4_1_1++) {
iterationContext.addContext(new IterationContext(l4_1_1.get(i4_1_1)));
MObject e4_1_1 = l4_1_1.get(i4_1_1);
m4_1_1_1(e4_1_1, i4_1_1, l4_1_1.size(), iterationContext);
m4_1_1_2(e4_1_1, i4_1_1, l4_1_1.size(), iterationContext);
m4_1_1_3(e4_1_1, i4_1_1, l4_1_1.size(), iterationContext);
m4_1_1_4(e4_1_1, i4_1_1, l4_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1*/


/* TableCellType - 4_1_1_1 - InstanceName */
private void m4_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_1 = new NodeInstance();
n4_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n4_1_1_1.setContext (activationContext);
n4_1_1_1.setParameter ("insertionEnabled", true);
n4_1_1_1.setParameter ("alignment", "LEFT");
n4_1_1_1.setParameter ("text", "$Name");
n4_1_1_1.setParameter ("paragraphStyle", "Normal");
n4_1_1_1.setParameter ("characterStyle", "None");
n4_1_1_1.setParameter ("columnIndex", 0);
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_1*/


/* ExternDocumentNavigationType - 4_1_1_2 - Description */
private void m4_1_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_2 = new NodeInstance();
n4_1_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType");
n4_1_1_2.setContext (activationContext);
n4_1_1_2.setInputMetaclass(Instance.class);
n4_1_1_2.setOutputMetaclass(ExternDocument.class);
n4_1_1_2.setParameter ("sort", false);
n4_1_1_2.setParameter ("externDocName", "description");
n4_1_1_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_2 = nb.navigate(n4_1_1_2, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_2);
for (int i4_1_1_2 = 0; i4_1_1_2 < l4_1_1_2.size(); i4_1_1_2++) {
iterationContext.addContext(new IterationContext(l4_1_1_2.get(i4_1_1_2)));
MObject e4_1_1_2 = l4_1_1_2.get(i4_1_1_2);
m4_1_1_2_1(e4_1_1_2, i4_1_1_2, l4_1_1_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_2*/


/* TableCellType - 4_1_1_2_1 - DescriptionCell */
private void m4_1_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_2_1 = new NodeInstance();
n4_1_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n4_1_1_2_1.setContext (activationContext);
n4_1_1_2_1.setParameter ("insertionEnabled", true);
n4_1_1_2_1.setParameter ("alignment", "LEFT");
n4_1_1_2_1.setParameter ("text", "$Content");
n4_1_1_2_1.setParameter ("paragraphStyle", "Normal");
n4_1_1_2_1.setParameter ("characterStyle", "None");
n4_1_1_2_1.setParameter ("columnIndex", 1);
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_2_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_2_1*/


/* SmartNavigationType - 4_1_1_3 - Classifier */
private void m4_1_1_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_3 = new NodeInstance();
n4_1_1_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1_3.setContext (activationContext);
n4_1_1_3.setInputMetaclass(Instance.class);
n4_1_1_3.setOutputMetaclass(Classifier.class);
n4_1_1_3.setParameter ("sort", false);
n4_1_1_3.setParameter ("outputStereotype", "None");
n4_1_1_3.setParameter ("relation", "Base");
n4_1_1_3.setParameter ("sequenceMode", true);
n4_1_1_3.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_3.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_3 = nb.navigate(n4_1_1_3, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_3);
for (int i4_1_1_3 = 0; i4_1_1_3 < l4_1_1_3.size(); i4_1_1_3++) {
iterationContext.addContext(new IterationContext(l4_1_1_3.get(i4_1_1_3)));
MObject e4_1_1_3 = l4_1_1_3.get(i4_1_1_3);
m4_1_1_3_1(e4_1_1_3, i4_1_1_3, l4_1_1_3.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_3", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_3*/


/* TableCellType - 4_1_1_3_1 - ClassifierName */
private void m4_1_1_3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_3_1 = new NodeInstance();
n4_1_1_3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n4_1_1_3_1.setContext (activationContext);
n4_1_1_3_1.setParameter ("insertionEnabled", true);
n4_1_1_3_1.setParameter ("alignment", "LEFT");
n4_1_1_3_1.setParameter ("text", "$Name");
n4_1_1_3_1.setParameter ("paragraphStyle", "Normal");
n4_1_1_3_1.setParameter ("characterStyle", "None");
n4_1_1_3_1.setParameter ("columnIndex", 2);
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_3_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_3_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_3_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_3_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_3_1*/


/* SmartNavigationType - 4_1_1_4 - CommunicationNodes */
private void m4_1_1_4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4 = new NodeInstance();
n4_1_1_4.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1_4.setContext (activationContext);
n4_1_1_4.setInputMetaclass(Instance.class);
n4_1_1_4.setOutputMetaclass(CommunicationNode.class);
n4_1_1_4.setParameter ("sort", false);
n4_1_1_4.setParameter ("outputStereotype", "None");
n4_1_1_4.setParameter ("relation", "RepresentedCommunicationNode");
n4_1_1_4.setParameter ("sequenceMode", true);
n4_1_1_4.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_4.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_4 = nb.navigate(n4_1_1_4, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_4);
for (int i4_1_1_4 = 0; i4_1_1_4 < l4_1_1_4.size(); i4_1_1_4++) {
iterationContext.addContext(new IterationContext(l4_1_1_4.get(i4_1_1_4)));
MObject e4_1_1_4 = l4_1_1_4.get(i4_1_1_4);
m4_1_1_4_1(e4_1_1_4, i4_1_1_4, l4_1_1_4.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4*/


/* SmartNavigationType - 4_1_1_4_1 - CommunicationInteractions */
private void m4_1_1_4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4_1 = new NodeInstance();
n4_1_1_4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1_4_1.setContext (activationContext);
n4_1_1_4_1.setInputMetaclass(CommunicationNode.class);
n4_1_1_4_1.setOutputMetaclass(CommunicationInteraction.class);
n4_1_1_4_1.setParameter ("sort", false);
n4_1_1_4_1.setParameter ("outputStereotype", "None");
n4_1_1_4_1.setParameter ("relation", "Owner");
n4_1_1_4_1.setParameter ("sequenceMode", true);
n4_1_1_4_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_4_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_4_1 = nb.navigate(n4_1_1_4_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_4_1);
for (int i4_1_1_4_1 = 0; i4_1_1_4_1 < l4_1_1_4_1.size(); i4_1_1_4_1++) {
iterationContext.addContext(new IterationContext(l4_1_1_4_1.get(i4_1_1_4_1)));
MObject e4_1_1_4_1 = l4_1_1_4_1.get(i4_1_1_4_1);
m4_1_1_4_1_1(e4_1_1_4_1, i4_1_1_4_1, l4_1_1_4_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4_1*/


/* SmartNavigationType - 4_1_1_4_1_1 - Collaborations */
private void m4_1_1_4_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4_1_1 = new NodeInstance();
n4_1_1_4_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1_4_1_1.setContext (activationContext);
n4_1_1_4_1_1.setInputMetaclass(CommunicationInteraction.class);
n4_1_1_4_1_1.setOutputMetaclass(Collaboration.class);
n4_1_1_4_1_1.setParameter ("sort", false);
n4_1_1_4_1_1.setParameter ("outputStereotype", "None");
n4_1_1_4_1_1.setParameter ("relation", "Owner");
n4_1_1_4_1_1.setParameter ("sequenceMode", true);
n4_1_1_4_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_4_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_4_1_1 = nb.navigate(n4_1_1_4_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_4_1_1);
for (int i4_1_1_4_1_1 = 0; i4_1_1_4_1_1 < l4_1_1_4_1_1.size(); i4_1_1_4_1_1++) {
iterationContext.addContext(new IterationContext(l4_1_1_4_1_1.get(i4_1_1_4_1_1)));
MObject e4_1_1_4_1_1 = l4_1_1_4_1_1.get(i4_1_1_4_1_1);
m4_1_1_4_1_1_1(e4_1_1_4_1_1, i4_1_1_4_1_1, l4_1_1_4_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4_1_1*/


/* TableCellType - 4_1_1_4_1_1_1 - ScenariiCell */
private void m4_1_1_4_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4_1_1_1 = new NodeInstance();
n4_1_1_4_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n4_1_1_4_1_1_1.setContext (activationContext);
n4_1_1_4_1_1_1.setParameter ("insertionEnabled", true);
n4_1_1_4_1_1_1.setParameter ("alignment", "LEFT");
n4_1_1_4_1_1_1.setParameter ("text", "");
n4_1_1_4_1_1_1.setParameter ("paragraphStyle", "Normal");
n4_1_1_4_1_1_1.setParameter ("characterStyle", "None");
n4_1_1_4_1_1_1.setParameter ("columnIndex", 3);
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_4_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_4_1_1_1, elt, index, maxIndex, iterationContext);
m4_1_1_4_1_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_4_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4_1_1_1*/


/* CommaSeparatedListType - 4_1_1_4_1_1_1_1 - ,  */
private void m4_1_1_4_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4_1_1_1_1 = new NodeInstance();
n4_1_1_4_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_1_1_4_1_1_1_1.setContext (activationContext);
n4_1_1_4_1_1_1_1.setParameter ("text", "");
n4_1_1_4_1_1_1_1.setParameter ("startSeparator", "");
n4_1_1_4_1_1_1_1.setParameter ("characterStyle", "None");
n4_1_1_4_1_1_1_1.setParameter ("separator", ", ");
n4_1_1_4_1_1_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_4_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_4_1_1_1_1, elt, index, maxIndex, iterationContext);
m4_1_1_4_1_1_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_4_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4_1_1_1_1*/


/* CharacterType - 4_1_1_4_1_1_1_1_1 - ScenarioName */
private void m4_1_1_4_1_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_4_1_1_1_1_1 = new NodeInstance();
n4_1_1_4_1_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_1_1_4_1_1_1_1_1.setContext (activationContext);
n4_1_1_4_1_1_1_1_1.setParameter ("text", "$Name");
n4_1_1_4_1_1_1_1_1.setParameter ("characterStyle", "None");
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_4_1_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_4_1_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_4_1_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_4_1_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 4_1_1_4_1_1_1_1_1*/


/* ProcedureType - 5 - MessageTable */
private void m5(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m5_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5*/


/* TableType - 5_1 - MessageTable */
private void m5_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1 = new NodeInstance();
n5_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableNode.TableType");
n5_1.setContext (activationContext);
n5_1.setParameter ("headerTitle19", "");
n5_1.setParameter ("headerTitle18", "");
n5_1.setParameter ("headerTitle17", "");
n5_1.setParameter ("headerTitle16", "");
n5_1.setParameter ("headerTitle39", "");
n5_1.setParameter ("headerTitle38", "");
n5_1.setParameter ("headerTitle36", "");
n5_1.setParameter ("headerTitle10", "");
n5_1.setParameter ("headerTitle37", "");
n5_1.setParameter ("headerTitle11", "");
n5_1.setParameter ("headerTitle34", "");
n5_1.setParameter ("headerTitle35", "");
n5_1.setParameter ("headerTitle32", "");
n5_1.setParameter ("headerTitle14", "");
n5_1.setParameter ("headerTitle33", "");
n5_1.setParameter ("headerTitle0", "Classe");
n5_1.setParameter ("tableWithHeader", true);
n5_1.setParameter ("headerTitle15", "");
n5_1.setParameter ("headerTitle30", "");
n5_1.setParameter ("headerTitle1", "Message(s) reçu(s)");
n5_1.setParameter ("headerTitle12", "");
n5_1.setParameter ("headerTitle31", "");
n5_1.setParameter ("headerTitle2", "");
n5_1.setParameter ("headerTitle13", "");
n5_1.setParameter ("headerTitle3", "");
n5_1.setParameter ("headerTitle4", "");
n5_1.setParameter ("headerAlignment", "CENTER");
n5_1.setParameter ("headerTitle5", "");
n5_1.setParameter ("headerTitle6", "");
n5_1.setParameter ("headerTitle7", "");
n5_1.setParameter ("headerTitle8", "");
n5_1.setParameter ("headerTitle9", "");
n5_1.setParameter ("headerTitle49", "");
n5_1.setParameter ("nbLines", 2);
n5_1.setParameter ("tableStyle", "ListeclaireAccent1");
n5_1.setParameter ("caption", "");
n5_1.setParameter ("headerTitle28", "");
n5_1.setParameter ("headerTitle27", "");
n5_1.setParameter ("headerTitle29", "");
n5_1.setParameter ("headerTitle23", "");
n5_1.setParameter ("headerTitle24", "");
n5_1.setParameter ("headerTitle25", "");
n5_1.setParameter ("headerTitle26", "");
n5_1.setParameter ("headerTitle20", "");
n5_1.setParameter ("headerTitle40", "");
n5_1.setParameter ("headerTitle21", "");
n5_1.setParameter ("horizontal", true);
n5_1.setParameter ("headerTitle22", "");
n5_1.setParameter ("tableAlignment", "BOTH");
n5_1.setParameter ("headerTitle42", "");
n5_1.setParameter ("headerTitle41", "");
n5_1.setParameter ("headerTitle44", "");
n5_1.setParameter ("headerTitle43", "");
n5_1.setParameter ("headerTitle46", "");
n5_1.setParameter ("headerTitle45", "");
n5_1.setParameter ("headerTitle48", "");
n5_1.setParameter ("headerTitle47", "");
IProductionBehavior pb = ((IProductionBehavior)n5_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n5_1, elt, index, maxIndex, iterationContext);
m5_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n5_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1*/


/* SmartNavigationType - 5_1_1 - Classifiers */
private void m5_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1 = new NodeInstance();
n5_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n5_1_1.setContext (activationContext);
n5_1_1.setInputMetaclass(Package.class);
n5_1_1.setOutputMetaclass(Classifier.class);
n5_1_1.setParameter ("sort", false);
n5_1_1.setParameter ("outputStereotype", "None");
n5_1_1.setParameter ("relation", "OwnedElement");
n5_1_1.setParameter ("sequenceMode", true);
n5_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n5_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l5_1_1 = nb.navigate(n5_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l5_1_1);
for (int i5_1_1 = 0; i5_1_1 < l5_1_1.size(); i5_1_1++) {
iterationContext.addContext(new IterationContext(l5_1_1.get(i5_1_1)));
MObject e5_1_1 = l5_1_1.get(i5_1_1);
m5_1_1_1(e5_1_1, i5_1_1, l5_1_1.size(), iterationContext);
m5_1_1_2(e5_1_1, i5_1_1, l5_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1*/


/* TableCellType - 5_1_1_1 - ClassifierCell */
private void m5_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_1 = new NodeInstance();
n5_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n5_1_1_1.setContext (activationContext);
n5_1_1_1.setParameter ("insertionEnabled", true);
n5_1_1_1.setParameter ("alignment", "LEFT");
n5_1_1_1.setParameter ("text", "$Name");
n5_1_1_1.setParameter ("paragraphStyle", "Normal");
n5_1_1_1.setParameter ("characterStyle", "None");
n5_1_1_1.setParameter ("columnIndex", 0);
IProductionBehavior pb = ((IProductionBehavior)n5_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n5_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n5_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_1*/


/* TableCellType - 5_1_1_2 - MessageCell */
private void m5_1_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_2 = new NodeInstance();
n5_1_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.TableCell.TableCellType");
n5_1_1_2.setContext (activationContext);
n5_1_1_2.setParameter ("insertionEnabled", true);
n5_1_1_2.setParameter ("alignment", "LEFT");
n5_1_1_2.setParameter ("text", "");
n5_1_1_2.setParameter ("paragraphStyle", "Normal");
n5_1_1_2.setParameter ("characterStyle", "None");
n5_1_1_2.setParameter ("columnIndex", 1);
IProductionBehavior pb = ((IProductionBehavior)n5_1_1_2.getNodeType ().getNodeBehavior ());
pb.beginProduction(n5_1_1_2, elt, index, maxIndex, iterationContext);
m5_1_1_2_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n5_1_1_2, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_2*/


/* SmartNavigationType - 5_1_1_2_1 - Instances */
private void m5_1_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_2_1 = new NodeInstance();
n5_1_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n5_1_1_2_1.setContext (activationContext);
n5_1_1_2_1.setInputMetaclass(Classifier.class);
n5_1_1_2_1.setOutputMetaclass(Instance.class);
n5_1_1_2_1.setParameter ("sort", false);
n5_1_1_2_1.setParameter ("outputStereotype", "None");
n5_1_1_2_1.setParameter ("relation", "Representing");
n5_1_1_2_1.setParameter ("sequenceMode", true);
n5_1_1_2_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n5_1_1_2_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l5_1_1_2_1 = nb.navigate(n5_1_1_2_1, elt, index, maxIndex, iterationContext);
filterNodoc(l5_1_1_2_1);
for (int i5_1_1_2_1 = 0; i5_1_1_2_1 < l5_1_1_2_1.size(); i5_1_1_2_1++) {
iterationContext.addContext(new IterationContext(l5_1_1_2_1.get(i5_1_1_2_1)));
MObject e5_1_1_2_1 = l5_1_1_2_1.get(i5_1_1_2_1);
m5_1_1_2_1_1(e5_1_1_2_1, i5_1_1_2_1, l5_1_1_2_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_2_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_2_1*/


/* SmartNavigationType - 5_1_1_2_1_1 - CommunicationNodes */
private void m5_1_1_2_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_2_1_1 = new NodeInstance();
n5_1_1_2_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n5_1_1_2_1_1.setContext (activationContext);
n5_1_1_2_1_1.setInputMetaclass(Instance.class);
n5_1_1_2_1_1.setOutputMetaclass(CommunicationNode.class);
n5_1_1_2_1_1.setParameter ("sort", false);
n5_1_1_2_1_1.setParameter ("outputStereotype", "None");
n5_1_1_2_1_1.setParameter ("relation", "RepresentedCommunicationNode");
n5_1_1_2_1_1.setParameter ("sequenceMode", true);
n5_1_1_2_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n5_1_1_2_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l5_1_1_2_1_1 = nb.navigate(n5_1_1_2_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l5_1_1_2_1_1);
for (int i5_1_1_2_1_1 = 0; i5_1_1_2_1_1 < l5_1_1_2_1_1.size(); i5_1_1_2_1_1++) {
iterationContext.addContext(new IterationContext(l5_1_1_2_1_1.get(i5_1_1_2_1_1)));
MObject e5_1_1_2_1_1 = l5_1_1_2_1_1.get(i5_1_1_2_1_1);
m5_1_1_2_1_1_1(e5_1_1_2_1_1, i5_1_1_2_1_1, l5_1_1_2_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_2_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_2_1_1*/


/* JythonType - 5_1_1_2_1_1_1 - IncomingMessages */
private void m5_1_1_2_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_2_1_1_1 = new NodeInstance();
n5_1_1_2_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.JythonNode.JythonType");
n5_1_1_2_1_1_1.setContext (activationContext);
n5_1_1_2_1_1_1.setInputMetaclass(CommunicationNode.class);
n5_1_1_2_1_1_1.setOutputMetaclass(CommunicationMessage.class);
n5_1_1_2_1_1_1.setParameter ("sort", false);
n5_1_1_2_1_1_1.setParameter ("jythonCode", "# This function must return an element or an array of elements.\r\n# elt the current element the node is executed on.\r\n# index the index of \"elt\" in the parent node return list.\r\n# maxIndex the last possible index in the parent node return list.\r\n# ctx the iteration context.\r\ndef navigate(elt, index, maxIndex, ctx):\r\n  messages = set()\r\n  for communicationChannel in elt.getStarted():\r\n     messages |=  set(communicationChannel.getEndToStartMessage())\r\n  for communicationChannel in elt.getEnded():\r\n     messages |= set(communicationChannel.getStartToEndMessage())\r\n  return messages");
n5_1_1_2_1_1_1.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n5_1_1_2_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l5_1_1_2_1_1_1 = nb.navigate(n5_1_1_2_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l5_1_1_2_1_1_1);
for (int i5_1_1_2_1_1_1 = 0; i5_1_1_2_1_1_1 < l5_1_1_2_1_1_1.size(); i5_1_1_2_1_1_1++) {
iterationContext.addContext(new IterationContext(l5_1_1_2_1_1_1.get(i5_1_1_2_1_1_1)));
MObject e5_1_1_2_1_1_1 = l5_1_1_2_1_1_1.get(i5_1_1_2_1_1_1);
m5_1_1_2_1_1_1_1(e5_1_1_2_1_1_1, i5_1_1_2_1_1_1, l5_1_1_2_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_2_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_2_1_1_1*/


/* ParagraphType - 5_1_1_2_1_1_1_1 - MessageName */
private void m5_1_1_2_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n5_1_1_2_1_1_1_1 = new NodeInstance();
n5_1_1_2_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n5_1_1_2_1_1_1_1.setContext (activationContext);
n5_1_1_2_1_1_1_1.setParameter ("text", "$Name");
n5_1_1_2_1_1_1_1.setParameter ("paragraphStyle", "Paragraphedeliste");
n5_1_1_2_1_1_1_1.setParameter ("characterStyle", "None");
n5_1_1_2_1_1_1_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n5_1_1_2_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n5_1_1_2_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n5_1_1_2_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("5_1_1_2_1_1_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 5_1_1_2_1_1_1_1*/


/* ProcedureType - 6 - AllDiagrams */
private void m6(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m6_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("6", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 6*/


/* SmartNavigationType - 6_1 - Diagrams */
private void m6_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n6_1 = new NodeInstance();
n6_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n6_1.setContext (activationContext);
n6_1.setInputMetaclass(Package.class);
n6_1.setOutputMetaclass(AbstractDiagram.class);
n6_1.setParameter ("sort", false);
n6_1.setParameter ("outputStereotype", "None");
n6_1.setParameter ("relation", "Product");
n6_1.setParameter ("sequenceMode", true);
n6_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n6_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l6_1 = nb.navigate(n6_1, elt, index, maxIndex, iterationContext);
filterNodoc(l6_1);
for (int i6_1 = 0; i6_1 < l6_1.size(); i6_1++) {
iterationContext.addContext(new IterationContext(l6_1.get(i6_1)));
MObject e6_1 = l6_1.get(i6_1);
m6_1_1(e6_1, i6_1, l6_1.size(), iterationContext);
m6_1_2(e6_1, i6_1, l6_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("6_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 6_1*/


/* DiagramType - 6_1_1 - Diagram */
private void m6_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n6_1_1 = new NodeInstance();
n6_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType");
n6_1_1.setContext (activationContext);
n6_1_1.setParameter ("paragraphStyle", "Normal");
n6_1_1.setParameter ("isMapSpecified", false);
n6_1_1.setParameter ("resizingPolicy", "DOCUMENT");
n6_1_1.setParameter ("hasProduced", false);
n6_1_1.setParameter ("mapping", "# This function is called when computing hyperlinks on this diagram.\r\n# It must return a valid element, or 'None'.\r\n# elt the element reprensented in the diagram.\r\n# diagram the diagram the element is unmasked in.\r\ndef getMapping(self, elt, diagram):\r\n\treturn elt\r\n");
n6_1_1.setParameter ("caption", "$Name");
IProductionBehavior pb = ((IProductionBehavior)n6_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n6_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n6_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("6_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 6_1_1*/


/* NoteNavigationType - 6_1_2 - DiagramDescription */
private void m6_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n6_1_2 = new NodeInstance();
n6_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n6_1_2.setContext (activationContext);
n6_1_2.setInputMetaclass(ClassDiagram.class);
n6_1_2.setOutputMetaclass(Note.class);
n6_1_2.setParameter ("noteName", "description");
n6_1_2.setParameter ("sort", false);
n6_1_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n6_1_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l6_1_2 = nb.navigate(n6_1_2, elt, index, maxIndex, iterationContext);
filterNodoc(l6_1_2);
for (int i6_1_2 = 0; i6_1_2 < l6_1_2.size(); i6_1_2++) {
iterationContext.addContext(new IterationContext(l6_1_2.get(i6_1_2)));
MObject e6_1_2 = l6_1_2.get(i6_1_2);
m6_1_2_1(e6_1_2, i6_1_2, l6_1_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("6_1_2", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 6_1_2*/


/* ParagraphType - 6_1_2_1 - DiagramDescription */
private void m6_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n6_1_2_1 = new NodeInstance();
n6_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n6_1_2_1.setContext (activationContext);
n6_1_2_1.setParameter ("text", "$Content");
n6_1_2_1.setParameter ("paragraphStyle", "Normal");
n6_1_2_1.setParameter ("characterStyle", "None");
n6_1_2_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n6_1_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n6_1_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n6_1_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("6_1_2_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 6_1_2_1*/


/* ProcedureType - 7 - AllPackages */
private void m7(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m7_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("7", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 7*/


/* SmartNavigationType - 7_1 - Metamodel Navigation */
private void m7_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n7_1 = new NodeInstance();
n7_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n7_1.setContext (activationContext);
n7_1.setInputMetaclass(Package.class);
n7_1.setOutputMetaclass(Package.class);
n7_1.setParameter ("sort", false);
n7_1.setParameter ("outputStereotype", "None");
n7_1.setParameter ("relation", "OwnedElement");
n7_1.setParameter ("sequenceMode", true);
n7_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n7_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l7_1 = nb.navigate(n7_1, elt, index, maxIndex, iterationContext);
filterNodoc(l7_1);
for (int i7_1 = 0; i7_1 < l7_1.size(); i7_1++) {
iterationContext.addContext(new IterationContext(l7_1.get(i7_1)));
MObject e7_1 = l7_1.get(i7_1);
m7_1_1(e7_1, i7_1, l7_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("7_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 7_1*/


/* SectionType - 7_1_1 - Section */
private void m7_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n7_1_1 = new NodeInstance();
n7_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n7_1_1.setContext (activationContext);
n7_1_1.setParameter ("startOnNewPage", false);
n7_1_1.setParameter ("text", "$Name");
n7_1_1.setParameter ("removeEmptySection", true);
n7_1_1.setParameter ("sectionStyle", "Titre n+1");
n7_1_1.setParameter ("numbering", true);
n7_1_1.setParameter ("showIcon", false);
n7_1_1.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n7_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n7_1_1, elt, index, maxIndex, iterationContext);
m2(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n7_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("7_1_1", "TemplateClassesEtInstances_1_1", e.getLocalizedMessage());
}
} /* END 7_1_1*/

}
