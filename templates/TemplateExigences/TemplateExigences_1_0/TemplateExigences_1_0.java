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
import com.modelio.module.documentpublisher.nodes.production.ExternDocumentNode.ExternDocumentType;
import com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType;
import com.modelio.module.documentpublisher.nodes.production.ReferenceNode.ReferenceType;
import com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType;
import com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType;
import com.modelio.module.documentpublisher.nodes.other.ProcedureNode.ProcedureType;
import com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType;
import com.modelio.module.documentpublisher.nodes.production.analystpropertytable.AnalystPropertyTableType;
import com.modelio.module.documentpublisher.nodes.other.NodeCallNode.NodeCallType;
import com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType;
import com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType;
import com.modelio.module.documentpublisher.nodes.navigation.SmartFinderNode.SmartFinderType;
import com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType;
import com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType;
import com.modelio.module.documentpublisher.nodes.other.DummyNode.DummyNodeType;
import com.modelio.module.documentpublisher.nodes.other.RootNode.RootType;

public class TemplateExigences_1_0 implements ITemplate {

private void loadAllNodes() {
  NodeManager nodeManager = NodeManager.getInstance ();
List<INodeType> controls = new ArrayList<> ();
controls.add (new com.modelio.module.documentpublisher.nodes.production.ExternDocumentNode.ExternDocumentType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.ReferenceNode.ReferenceType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.ProcedureNode.ProcedureType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.analystpropertytable.AnalystPropertyTableType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.NodeCallNode.NodeCallType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.SmartFinderNode.SmartFinderType ());
controls.add (new com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType ());
controls.add (new com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.DummyNode.DummyNodeType ());
controls.add (new com.modelio.module.documentpublisher.nodes.other.RootNode.RootType ());
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

public TemplateExigences_1_0() {
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
description += "Ce template est initalisé avec le template \"Exigences\" fourni par modelio mais il sera modifié pour être adapté au besoin de l'UJF\r";
description += "\r";
description += "--------------------------------\r";
description += "Objectif: Analyse des exigences.\r";
description += "Applicable sur: Dossier d'exigences.\r";
description += "Quand: Au début d'un projet.\r";
description += "\r";
description += "Documente la nature des exigences et leurs propriétés.\r";
description += "N'oubliez pas de produire un document à chaque packaging d'un RAMC d'exigences.\r";
description += "Combinaison intéressante avec les plan-types \"Use Cases\" et \"Matrice de Traçabilité\".";
    return description;
}

@Override
public String getTemplateName() {
    return "TemplateExigences_1_0";
}

public boolean activate(String baseFile, String targetFile, List<ModelElement>l1, GenerationMode mode, Target target, int titleLevel, List<DocumentContent> docContent, List<Revision> revisions) throws TemplateNodeException, FormatNotImplementedException {
logger.info("TemplateExigences_1_0 activated at " + Calendar.getInstance().getTime());
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
n1.setParameter ("creationDate", "Fri Feb 29 11:03:18 CET 2008");
n1.setParameter ("description", "Ce template est initalisé avec le template \"Exigences\" fourni par modelio mais il sera modifié pour être adapté au besoin de l'UJF\r\n\r\n--------------------------------\r\nObjectif: Analyse des exigences.\r\nApplicable sur: Dossier d'exigences.\r\nQuand: Au début d'un projet.\r\n\r\nDocumente la nature des exigences et leurs propriétés.\r\nN'oubliez pas de produire un document à chaque packaging d'un RAMC d'exigences.\r\nCombinaison intéressante avec les plan-types \"Use Cases\" et \"Matrice de Traçabilité\".");
n1.setParameter ("templateparameters", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAKdwQAAAAK\r\nc3IATWNvbS5tb2RlbGlvLm1vZHVsZS5kb2N1bWVudHB1Ymxpc2hlci5ub2Rlcy50ZW1wbGF0ZS5j\r\nb250ZXh0LlRlbXBsYXRlUGFyYW1ldGVyIihydAjuqx0CAAVaAAtwcm9wYWdhdGlvbkwADGRlZmF1\r\nbHRWYWx1ZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAC2Rlc2NyaXB0aW9ucQB+AANMAA5lZmZlY3Rp\r\ndmVWYWx1ZXEAfgADTAAEbmFtZXEAfgADeHABdAAIRG9jdW1lbnR0AA5Eb2N1bWVudCB0aXRsZXQA\r\nAHQABVRpdGxlc3EAfgACAXQAB1N1YmplY3R0ABBEb2N1bWVudCBzdWJqZWN0cQB+AAdxAH4ACnNx\r\nAH4AAgF0AAhDYXRlZ29yeXQAEURvY3VtZW50IGNhdGVnb3J5cQB+AAdxAH4ADXNxAH4AAgF0AAVE\r\ncmFmdHQAD0RvY3VtZW50IHN0YXR1c3EAfgAHdAAGU3RhdHVzc3EAfgACAXQAEURvY3VtZW50UHVi\r\nbGlzaGVydAAPRG9jdW1lbnQgYXV0aG9ycQB+AAd0AAZBdXRob3JzcQB+AAIBdAADMS4wdAAQRG9j\r\ndW1lbnQgdmVyc2lvbnEAfgAHdAAHVmVyc2lvbnNxAH4AAgF0AAtNb2RlbGlvc29mdHQAEERvY3Vt\r\nZW50IGNvbXBhbnlxAH4AB3QAB0NvbXBhbnlzcQB+AAIBcQB+AAd0ABBEb2N1bWVudCBhZGRyZXNz\r\ncQB+AAd0AAdBZGRyZXNzc3EAfgACAXEAfgAHdAASRG9jdW1lbnQgY29weXJpZ2h0cQB+AAd0AAlD\r\nb3B5cmlnaHRzcQB+AAIBdAABM3QAJk1heGltdW0gZGVwdGggb2YgdGhlIHRhYmxlIG9mIGNvbnRl\r\nbnRzcQB+AAd0AAlUT0MgRGVwdGh4");
n1.setParameter ("modificationDate", "Wed Apr 02 18:28:18 CEST 2014");
n1.setParameter ("baseFile", "");
n1.setParameter ("targetFile", "");
n1.setParameter ("version", "1.0");
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
}
if (rb.endProduction(n1, null)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
logger.info("TemplateExigences_1_0 completed at" + Calendar.getInstance().getTime());
return true;
}


/* RootType - 1 - TemplateExigences_1_0 */
private void m1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m2(elt, index, maxIndex, iterationContext);
m1_2(elt, index, maxIndex, iterationContext);
m1_3(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1*/


/* SmartFinderType - 1_2 - Find All Requirement Containers */
private void m1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_2 = new NodeInstance();
n1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartFinderNode.SmartFinderType");
n1_2.setContext (activationContext);
n1_2.setInputMetaclass(RequirementContainer.class);
n1_2.setOutputMetaclass(RequirementContainer.class);
n1_2.setParameter ("sort", false);
n1_2.setParameter ("outputStereotype", "None");
n1_2.setParameter ("sequenceMode", true);
n1_2.setParameter ("parentFilterStereotype", "None");
n1_2.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n1_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l1_2 = nb.navigate(n1_2, elt, index, maxIndex, iterationContext);
filterNodoc(l1_2);
for (int i1_2 = 0; i1_2 < l1_2.size(); i1_2++) {
iterationContext.addContext(new IterationContext(l1_2.get(i1_2)));
MObject e1_2 = l1_2.get(i1_2);
m2(e1_2, i1_2, l1_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_2*/


/* SectionType - 1_3 - SectionIndexOfTerms */
private void m1_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_3 = new NodeInstance();
n1_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n1_3.setContext (activationContext);
n1_3.setParameter ("startOnNewPage", true);
n1_3.setParameter ("text", "Index des exigences");
n1_3.setParameter ("removeEmptySection", true);
n1_3.setParameter ("sectionStyle", "Titre n");
n1_3.setParameter ("numbering", true);
n1_3.setParameter ("showIcon", false);
n1_3.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n1_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n1_3, elt, index, maxIndex, iterationContext);
m1_3_1(elt, index, maxIndex, iterationContext);
m1_3_2(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n1_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_3*/


/* ParagraphType - 1_3_1 - Description */
private void m1_3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_3_1 = new NodeInstance();
n1_3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n1_3_1.setContext (activationContext);
n1_3_1.setParameter ("text", "Cette section fourni un index alphabétique des exigences décrites dans les sections précédentes. Pour chaque exigence, un lien direct vers sa description détaillée est donné.");
n1_3_1.setParameter ("paragraphStyle", "Texte");
n1_3_1.setParameter ("characterStyle", "Policepardfaut");
n1_3_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n1_3_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n1_3_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n1_3_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_3_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_3_1*/


/* SmartFinderType - 1_3_2 - Find All Requirements */
private void m1_3_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_3_2 = new NodeInstance();
n1_3_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartFinderNode.SmartFinderType");
n1_3_2.setContext (activationContext);
n1_3_2.setInputMetaclass(RequirementContainer.class);
n1_3_2.setOutputMetaclass(Requirement.class);
n1_3_2.setParameter ("sort", true);
n1_3_2.setParameter ("outputStereotype", "None");
n1_3_2.setParameter ("sequenceMode", true);
n1_3_2.setParameter ("parentFilterStereotype", "None");
n1_3_2.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n1_3_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l1_3_2 = nb.navigate(n1_3_2, elt, index, maxIndex, iterationContext);
filterNodoc(l1_3_2);
for (int i1_3_2 = 0; i1_3_2 < l1_3_2.size(); i1_3_2++) {
iterationContext.addContext(new IterationContext(l1_3_2.get(i1_3_2)));
MObject e1_3_2 = l1_3_2.get(i1_3_2);
m1_3_2_1(e1_3_2, i1_3_2, l1_3_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_3_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_3_2*/


/* ParagraphType - 1_3_2_1 - RequirementReference */
private void m1_3_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_3_2_1 = new NodeInstance();
n1_3_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n1_3_2_1.setContext (activationContext);
n1_3_2_1.setParameter ("text", "");
n1_3_2_1.setParameter ("paragraphStyle", "Sansinterligne");
n1_3_2_1.setParameter ("characterStyle", "Policepardfaut");
n1_3_2_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n1_3_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n1_3_2_1, elt, index, maxIndex, iterationContext);
m1_3_2_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n1_3_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_3_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_3_2_1*/


/* ReferenceType - 1_3_2_1_1 */
private void m1_3_2_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n1_3_2_1_1 = new NodeInstance();
n1_3_2_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ReferenceNode.ReferenceType");
n1_3_2_1_1.setContext (activationContext);
n1_3_2_1_1.setParameter ("text", "$Name");
IProductionBehavior pb = ((IProductionBehavior)n1_3_2_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n1_3_2_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n1_3_2_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("1_3_2_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 1_3_2_1_1*/


/* ProcedureType - 2 - ProcContainerContent */
private void m2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m2_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2*/


/* SectionType - 2_1 - SectionNameOfContainer */
private void m2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1 = new NodeInstance();
n2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n2_1.setContext (activationContext);
n2_1.setParameter ("startOnNewPage", true);
n2_1.setParameter ("text", "$Name");
n2_1.setParameter ("removeEmptySection", true);
n2_1.setParameter ("sectionStyle", "Titre n");
n2_1.setParameter ("numbering", true);
n2_1.setParameter ("showIcon", false);
n2_1.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1, elt, index, maxIndex, iterationContext);
m2_1_1(elt, index, maxIndex, iterationContext);
m2_1_2(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1*/


/* SectionType - 2_1_1 - SectionContainerDescription */
private void m2_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1 = new NodeInstance();
n2_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n2_1_1.setContext (activationContext);
n2_1_1.setParameter ("startOnNewPage", false);
n2_1_1.setParameter ("text", "Description");
n2_1_1.setParameter ("removeEmptySection", true);
n2_1_1.setParameter ("sectionStyle", "Titre n+1");
n2_1_1.setParameter ("numbering", true);
n2_1_1.setParameter ("showIcon", false);
n2_1_1.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n2_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1, elt, index, maxIndex, iterationContext);
m2_1_1_1(elt, index, maxIndex, iterationContext);
m2_1_1_2(elt, index, maxIndex, iterationContext);
m2_1_1_3(elt, index, maxIndex, iterationContext);
m2_1_1_4(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1*/


/* ParagraphType - 2_1_1_1 - ContainerDescription */
private void m2_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_1 = new NodeInstance();
n2_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_1_1.setContext (activationContext);
n2_1_1_1.setParameter ("text", "$Definition");
n2_1_1_1.setParameter ("paragraphStyle", "Texte");
n2_1_1_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_1_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_1*/


/* NoteNavigationType - 2_1_1_2 - Get Description Note */
private void m2_1_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_2 = new NodeInstance();
n2_1_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n2_1_1_2.setContext (activationContext);
n2_1_1_2.setInputMetaclass(ModelElement.class);
n2_1_1_2.setOutputMetaclass(Note.class);
n2_1_1_2.setParameter ("noteName", "description");
n2_1_1_2.setParameter ("sort", false);
n2_1_1_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_1_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_1_2 = nb.navigate(n2_1_1_2, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_1_2);
for (int i2_1_1_2 = 0; i2_1_1_2 < l2_1_1_2.size(); i2_1_1_2++) {
iterationContext.addContext(new IterationContext(l2_1_1_2.get(i2_1_1_2)));
MObject e2_1_1_2 = l2_1_1_2.get(i2_1_1_2);
m2_1_1_2_1(e2_1_1_2, i2_1_1_2, l2_1_1_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_2*/


/* ParagraphType - 2_1_1_2_1 - Diagram Note Description */
private void m2_1_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_2_1 = new NodeInstance();
n2_1_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_1_2_1.setContext (activationContext);
n2_1_1_2_1.setParameter ("text", "$Content");
n2_1_1_2_1.setParameter ("paragraphStyle", "Texte");
n2_1_1_2_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_1_2_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_2_1*/


/* ExternDocumentNavigationType - 2_1_1_3 - Get Description RichNote */
private void m2_1_1_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_3 = new NodeInstance();
n2_1_1_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType");
n2_1_1_3.setContext (activationContext);
n2_1_1_3.setInputMetaclass(RequirementContainer.class);
n2_1_1_3.setOutputMetaclass(ExternDocument.class);
n2_1_1_3.setParameter ("sort", false);
n2_1_1_3.setParameter ("externDocName", "description");
n2_1_1_3.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_1_3.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_1_3 = nb.navigate(n2_1_1_3, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_1_3);
for (int i2_1_1_3 = 0; i2_1_1_3 < l2_1_1_3.size(); i2_1_1_3++) {
iterationContext.addContext(new IterationContext(l2_1_1_3.get(i2_1_1_3)));
MObject e2_1_1_3 = l2_1_1_3.get(i2_1_1_3);
m2_1_1_3_1(e2_1_1_3, i2_1_1_3, l2_1_1_3.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_3*/


/* ExternDocumentType - 2_1_1_3_1 - Note Riche */
private void m2_1_1_3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_3_1 = new NodeInstance();
n2_1_1_3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ExternDocumentNode.ExternDocumentType");
n2_1_1_3_1.setContext (activationContext);
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_3_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_3_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_3_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_3_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_3_1*/


/* SmartNavigationType - 2_1_1_4 - Get requirement diagrams */
private void m2_1_1_4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_4 = new NodeInstance();
n2_1_1_4.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n2_1_1_4.setContext (activationContext);
n2_1_1_4.setInputMetaclass(RequirementContainer.class);
n2_1_1_4.setOutputMetaclass(StaticDiagram.class);
n2_1_1_4.setParameter ("sort", false);
n2_1_1_4.setParameter ("outputStereotype", "requirement_diagram");
n2_1_1_4.setParameter ("relation", "Product");
n2_1_1_4.setParameter ("sequenceMode", true);
n2_1_1_4.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n2_1_1_4.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_1_4 = nb.navigate(n2_1_1_4, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_1_4);
for (int i2_1_1_4 = 0; i2_1_1_4 < l2_1_1_4.size(); i2_1_1_4++) {
iterationContext.addContext(new IterationContext(l2_1_1_4.get(i2_1_1_4)));
MObject e2_1_1_4 = l2_1_1_4.get(i2_1_1_4);
m2_1_1_4_1(e2_1_1_4, i2_1_1_4, l2_1_1_4.size(), iterationContext);
m2_1_1_4_2(e2_1_1_4, i2_1_1_4, l2_1_1_4.size(), iterationContext);
m2_1_1_4_3(e2_1_1_4, i2_1_1_4, l2_1_1_4.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_4", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_4*/


/* DiagramType - 2_1_1_4_1 - Requirement diagram */
private void m2_1_1_4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_4_1 = new NodeInstance();
n2_1_1_4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType");
n2_1_1_4_1.setContext (activationContext);
n2_1_1_4_1.setParameter ("paragraphStyle", "Texte");
n2_1_1_4_1.setParameter ("isMapSpecified", false);
n2_1_1_4_1.setParameter ("resizingPolicy", "DOCUMENT");
n2_1_1_4_1.setParameter ("hasProduced", false);
n2_1_1_4_1.setParameter ("mapping", "# This function is called when computing hyperlinks on this diagram.\r\n# It must return a valid element, or 'None'.\r\n# elt the element reprensented in the diagram.\r\n# diagram the diagram the element is unmasked in.\r\ndef getMapping(self, elt, diagram):\r\n\treturn elt\r\n");
n2_1_1_4_1.setParameter ("caption", "$Name");
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_4_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_4_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_4_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_4_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_4_1*/


/* NoteNavigationType - 2_1_1_4_2 - Get Description Note */
private void m2_1_1_4_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_4_2 = new NodeInstance();
n2_1_1_4_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n2_1_1_4_2.setContext (activationContext);
n2_1_1_4_2.setInputMetaclass(ModelElement.class);
n2_1_1_4_2.setOutputMetaclass(Note.class);
n2_1_1_4_2.setParameter ("noteName", "description");
n2_1_1_4_2.setParameter ("sort", false);
n2_1_1_4_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_1_4_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_1_4_2 = nb.navigate(n2_1_1_4_2, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_1_4_2);
for (int i2_1_1_4_2 = 0; i2_1_1_4_2 < l2_1_1_4_2.size(); i2_1_1_4_2++) {
iterationContext.addContext(new IterationContext(l2_1_1_4_2.get(i2_1_1_4_2)));
MObject e2_1_1_4_2 = l2_1_1_4_2.get(i2_1_1_4_2);
m2_1_1_4_2_1(e2_1_1_4_2, i2_1_1_4_2, l2_1_1_4_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_4_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_4_2*/


/* ParagraphType - 2_1_1_4_2_1 - Diagram Note Description */
private void m2_1_1_4_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_4_2_1 = new NodeInstance();
n2_1_1_4_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_1_4_2_1.setContext (activationContext);
n2_1_1_4_2_1.setParameter ("text", "$Content");
n2_1_1_4_2_1.setParameter ("paragraphStyle", "Texte");
n2_1_1_4_2_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_1_4_2_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_4_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_4_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_4_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_4_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_4_2_1*/


/* ParagraphType - 2_1_1_4_3 - CR */
private void m2_1_1_4_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_1_4_3 = new NodeInstance();
n2_1_1_4_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_1_4_3.setContext (activationContext);
n2_1_1_4_3.setParameter ("text", "");
n2_1_1_4_3.setParameter ("paragraphStyle", "Normal");
n2_1_1_4_3.setParameter ("characterStyle", "None");
n2_1_1_4_3.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_1_4_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_1_4_3, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_1_4_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_1_4_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_1_4_3*/


/* SectionType - 2_1_2 - SectionRequirements */
private void m2_1_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2 = new NodeInstance();
n2_1_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.SectionNode.SectionType");
n2_1_2.setContext (activationContext);
n2_1_2.setParameter ("startOnNewPage", false);
n2_1_2.setParameter ("text", "Liste des exigences");
n2_1_2.setParameter ("removeEmptySection", true);
n2_1_2.setParameter ("sectionStyle", "Titre n");
n2_1_2.setParameter ("numbering", true);
n2_1_2.setParameter ("showIcon", false);
n2_1_2.setParameter ("alternativeText", "");
IProductionBehavior pb = ((IProductionBehavior)n2_1_2.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2, elt, index, maxIndex, iterationContext);
m2_1_2_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2*/


/* SmartNavigationType - 2_1_2_1 - Foreach Requirement */
private void m2_1_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1 = new NodeInstance();
n2_1_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n2_1_2_1.setContext (activationContext);
n2_1_2_1.setInputMetaclass(RequirementContainer.class);
n2_1_2_1.setOutputMetaclass(Requirement.class);
n2_1_2_1.setParameter ("sort", false);
n2_1_2_1.setParameter ("outputStereotype", "None");
n2_1_2_1.setParameter ("relation", "OwnedRequirement");
n2_1_2_1.setParameter ("sequenceMode", true);
n2_1_2_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1 = nb.navigate(n2_1_2_1, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1);
for (int i2_1_2_1 = 0; i2_1_2_1 < l2_1_2_1.size(); i2_1_2_1++) {
iterationContext.addContext(new IterationContext(l2_1_2_1.get(i2_1_2_1)));
MObject e2_1_2_1 = l2_1_2_1.get(i2_1_2_1);
m2_1_2_1_1(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m4(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m2_1_2_1_3(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m2_1_2_1_4(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m2_1_2_1_5(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m2_1_2_1_6(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m2_1_2_1_7(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
m3(e2_1_2_1, i2_1_2_1, l2_1_2_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1*/


/* ParagraphType - 2_1_2_1_1 - NameOfRequirement */
private void m2_1_2_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_1 = new NodeInstance();
n2_1_2_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_2_1_1.setContext (activationContext);
n2_1_2_1_1.setBookmark(true);
n2_1_2_1_1.setParameter ("text", "$Name");
n2_1_2_1_1.setParameter ("paragraphStyle", "Soustitre");
n2_1_2_1_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_2_1_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_1*/


/* ParagraphType - 2_1_2_1_3 - DefinitionOfRequirement */
private void m2_1_2_1_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_3 = new NodeInstance();
n2_1_2_1_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_2_1_3.setContext (activationContext);
n2_1_2_1_3.setParameter ("text", "$Definition");
n2_1_2_1_3.setParameter ("paragraphStyle", "Paragraphedeliste");
n2_1_2_1_3.setParameter ("characterStyle", "Policepardfaut");
n2_1_2_1_3.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_3, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_3*/


/* NoteNavigationType - 2_1_2_1_4 - Get Description Note */
private void m2_1_2_1_4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_4 = new NodeInstance();
n2_1_2_1_4.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n2_1_2_1_4.setContext (activationContext);
n2_1_2_1_4.setInputMetaclass(ModelElement.class);
n2_1_2_1_4.setOutputMetaclass(Note.class);
n2_1_2_1_4.setParameter ("noteName", "description");
n2_1_2_1_4.setParameter ("sort", false);
n2_1_2_1_4.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1_4.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1_4 = nb.navigate(n2_1_2_1_4, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1_4);
for (int i2_1_2_1_4 = 0; i2_1_2_1_4 < l2_1_2_1_4.size(); i2_1_2_1_4++) {
iterationContext.addContext(new IterationContext(l2_1_2_1_4.get(i2_1_2_1_4)));
MObject e2_1_2_1_4 = l2_1_2_1_4.get(i2_1_2_1_4);
m2_1_2_1_4_1(e2_1_2_1_4, i2_1_2_1_4, l2_1_2_1_4.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_4", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_4*/


/* ParagraphType - 2_1_2_1_4_1 - Diagram Note Description */
private void m2_1_2_1_4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_4_1 = new NodeInstance();
n2_1_2_1_4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_2_1_4_1.setContext (activationContext);
n2_1_2_1_4_1.setParameter ("text", "$Content");
n2_1_2_1_4_1.setParameter ("paragraphStyle", "Texte");
n2_1_2_1_4_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_2_1_4_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_4_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_4_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_4_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_4_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_4_1*/


/* ExternDocumentNavigationType - 2_1_2_1_5 - Get Description RichNote */
private void m2_1_2_1_5(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_5 = new NodeInstance();
n2_1_2_1_5.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType");
n2_1_2_1_5.setContext (activationContext);
n2_1_2_1_5.setInputMetaclass(Requirement.class);
n2_1_2_1_5.setOutputMetaclass(ExternDocument.class);
n2_1_2_1_5.setParameter ("sort", false);
n2_1_2_1_5.setParameter ("externDocName", "description");
n2_1_2_1_5.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1_5.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1_5 = nb.navigate(n2_1_2_1_5, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1_5);
for (int i2_1_2_1_5 = 0; i2_1_2_1_5 < l2_1_2_1_5.size(); i2_1_2_1_5++) {
iterationContext.addContext(new IterationContext(l2_1_2_1_5.get(i2_1_2_1_5)));
MObject e2_1_2_1_5 = l2_1_2_1_5.get(i2_1_2_1_5);
m2_1_2_1_5_1(e2_1_2_1_5, i2_1_2_1_5, l2_1_2_1_5.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_5", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_5*/


/* ExternDocumentType - 2_1_2_1_5_1 - Note Riche */
private void m2_1_2_1_5_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_5_1 = new NodeInstance();
n2_1_2_1_5_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ExternDocumentNode.ExternDocumentType");
n2_1_2_1_5_1.setContext (activationContext);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_5_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_5_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_5_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_5_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_5_1*/


/* ExternDocumentNavigationType - 2_1_2_1_6 - Get Requirement RichNote */
private void m2_1_2_1_6(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_6 = new NodeInstance();
n2_1_2_1_6.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.ExternDocumentNavigationNode.ExternDocumentNavigationType");
n2_1_2_1_6.setContext (activationContext);
n2_1_2_1_6.setInputMetaclass(Requirement.class);
n2_1_2_1_6.setOutputMetaclass(ExternDocument.class);
n2_1_2_1_6.setParameter ("sort", false);
n2_1_2_1_6.setParameter ("externDocName", "requirement");
n2_1_2_1_6.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1_6.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1_6 = nb.navigate(n2_1_2_1_6, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1_6);
for (int i2_1_2_1_6 = 0; i2_1_2_1_6 < l2_1_2_1_6.size(); i2_1_2_1_6++) {
iterationContext.addContext(new IterationContext(l2_1_2_1_6.get(i2_1_2_1_6)));
MObject e2_1_2_1_6 = l2_1_2_1_6.get(i2_1_2_1_6);
m2_1_2_1_6_1(e2_1_2_1_6, i2_1_2_1_6, l2_1_2_1_6.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_6", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_6*/


/* ExternDocumentType - 2_1_2_1_6_1 - Note Riche */
private void m2_1_2_1_6_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_6_1 = new NodeInstance();
n2_1_2_1_6_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ExternDocumentNode.ExternDocumentType");
n2_1_2_1_6_1.setContext (activationContext);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_6_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_6_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_6_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_6_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_6_1*/


/* SmartNavigationType - 2_1_2_1_7 - Get requirement diagrams */
private void m2_1_2_1_7(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_7 = new NodeInstance();
n2_1_2_1_7.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n2_1_2_1_7.setContext (activationContext);
n2_1_2_1_7.setInputMetaclass(Requirement.class);
n2_1_2_1_7.setOutputMetaclass(StaticDiagram.class);
n2_1_2_1_7.setParameter ("sort", false);
n2_1_2_1_7.setParameter ("outputStereotype", "requirement_diagram");
n2_1_2_1_7.setParameter ("relation", "Product");
n2_1_2_1_7.setParameter ("sequenceMode", true);
n2_1_2_1_7.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1_7.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1_7 = nb.navigate(n2_1_2_1_7, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1_7);
for (int i2_1_2_1_7 = 0; i2_1_2_1_7 < l2_1_2_1_7.size(); i2_1_2_1_7++) {
iterationContext.addContext(new IterationContext(l2_1_2_1_7.get(i2_1_2_1_7)));
MObject e2_1_2_1_7 = l2_1_2_1_7.get(i2_1_2_1_7);
m2_1_2_1_7_1(e2_1_2_1_7, i2_1_2_1_7, l2_1_2_1_7.size(), iterationContext);
m2_1_2_1_7_2(e2_1_2_1_7, i2_1_2_1_7, l2_1_2_1_7.size(), iterationContext);
m2_1_2_1_7_3(e2_1_2_1_7, i2_1_2_1_7, l2_1_2_1_7.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_7", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_7*/


/* DiagramType - 2_1_2_1_7_1 - Requirement diagram */
private void m2_1_2_1_7_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_7_1 = new NodeInstance();
n2_1_2_1_7_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.DiagramNode.DiagramType");
n2_1_2_1_7_1.setContext (activationContext);
n2_1_2_1_7_1.setParameter ("paragraphStyle", "Texte");
n2_1_2_1_7_1.setParameter ("isMapSpecified", false);
n2_1_2_1_7_1.setParameter ("resizingPolicy", "DOCUMENT");
n2_1_2_1_7_1.setParameter ("hasProduced", false);
n2_1_2_1_7_1.setParameter ("mapping", "# This function is called when computing hyperlinks on this diagram.\r\n# It must return a valid element, or 'None'.\r\n# elt the element reprensented in the diagram.\r\n# diagram the diagram the element is unmasked in.\r\ndef getMapping(self, elt, diagram):\r\n\treturn elt\r\n");
n2_1_2_1_7_1.setParameter ("caption", "$Name");
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_7_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_7_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_7_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_7_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_7_1*/


/* NoteNavigationType - 2_1_2_1_7_2 - Get Description Note */
private void m2_1_2_1_7_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_7_2 = new NodeInstance();
n2_1_2_1_7_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.NoteNavigationNode.NoteNavigationType");
n2_1_2_1_7_2.setContext (activationContext);
n2_1_2_1_7_2.setInputMetaclass(ModelElement.class);
n2_1_2_1_7_2.setOutputMetaclass(Note.class);
n2_1_2_1_7_2.setParameter ("noteName", "description");
n2_1_2_1_7_2.setParameter ("sort", false);
n2_1_2_1_7_2.setParameter ("sequenceMode", true);
INavigationBehavior nb = ((INavigationBehavior)n2_1_2_1_7_2.getNodeType ().getNodeBehavior ());
List <? extends MObject> l2_1_2_1_7_2 = nb.navigate(n2_1_2_1_7_2, elt, index, maxIndex, iterationContext);
filterNodoc(l2_1_2_1_7_2);
for (int i2_1_2_1_7_2 = 0; i2_1_2_1_7_2 < l2_1_2_1_7_2.size(); i2_1_2_1_7_2++) {
iterationContext.addContext(new IterationContext(l2_1_2_1_7_2.get(i2_1_2_1_7_2)));
MObject e2_1_2_1_7_2 = l2_1_2_1_7_2.get(i2_1_2_1_7_2);
m2_1_2_1_7_2_1(e2_1_2_1_7_2, i2_1_2_1_7_2, l2_1_2_1_7_2.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_7_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_7_2*/


/* ParagraphType - 2_1_2_1_7_2_1 - Diagram Note Description */
private void m2_1_2_1_7_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_7_2_1 = new NodeInstance();
n2_1_2_1_7_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_2_1_7_2_1.setContext (activationContext);
n2_1_2_1_7_2_1.setParameter ("text", "$Content");
n2_1_2_1_7_2_1.setParameter ("paragraphStyle", "Texte");
n2_1_2_1_7_2_1.setParameter ("characterStyle", "Policepardfaut");
n2_1_2_1_7_2_1.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_7_2_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_7_2_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_7_2_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_7_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_7_2_1*/


/* ParagraphType - 2_1_2_1_7_3 - CR */
private void m2_1_2_1_7_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n2_1_2_1_7_3 = new NodeInstance();
n2_1_2_1_7_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n2_1_2_1_7_3.setContext (activationContext);
n2_1_2_1_7_3.setParameter ("text", "");
n2_1_2_1_7_3.setParameter ("paragraphStyle", "Normal");
n2_1_2_1_7_3.setParameter ("characterStyle", "None");
n2_1_2_1_7_3.setParameter ("removeEmptyParagraph", false);
IProductionBehavior pb = ((IProductionBehavior)n2_1_2_1_7_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n2_1_2_1_7_3, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n2_1_2_1_7_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("2_1_2_1_7_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 2_1_2_1_7_3*/


/* ProcedureType - 3 - ProcPropertyList */
private void m3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m3_1(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 3*/


/* AnalystPropertyTableType - 3_1 - Analyst Property Table */
private void m3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n3_1 = new NodeInstance();
n3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.analystpropertytable.AnalystPropertyTableType");
n3_1.setContext (activationContext);
n3_1.setParameter ("content", "CURRENT");
n3_1.setParameter ("tableAlignment", "LEFT");
n3_1.setParameter ("tableStyle", "TrameclaireAccent1");
n3_1.setParameter ("headerAlignment", "CENTER");
n3_1.setParameter ("caption", "$Name");
IProductionBehavior pb = ((IProductionBehavior)n3_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n3_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n3_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("3_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 3_1*/


/* ProcedureType - 4 - Dependencies */
private void m4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
m4_1(elt, index, maxIndex, iterationContext);
m4_2(elt, index, maxIndex, iterationContext);
m4_3(elt, index, maxIndex, iterationContext);
m4_4(elt, index, maxIndex, iterationContext);
m4_5(elt, index, maxIndex, iterationContext);
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4*/


/* ParagraphType - 4_1 - part of */
private void m4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1 = new NodeInstance();
n4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n4_1.setContext (activationContext);
n4_1.setParameter ("text", "");
n4_1.setParameter ("paragraphStyle", "Texte");
n4_1.setParameter ("characterStyle", "None");
n4_1.setParameter ("removeEmptyParagraph", true);
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
throw new TemplateNodeException("4_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_1*/


/* SmartNavigationType - 4_1_1 - DependsOnDependency - part */
private void m4_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1 = new NodeInstance();
n4_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1.setContext (activationContext);
n4_1_1.setInputMetaclass(Requirement.class);
n4_1_1.setOutputMetaclass(Dependency.class);
n4_1_1.setParameter ("sort", false);
n4_1_1.setParameter ("outputStereotype", "part");
n4_1_1.setParameter ("relation", "DependsOnDependency");
n4_1_1.setParameter ("sequenceMode", true);
n4_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1 = nb.navigate(n4_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1);
for (int i4_1_1 = 0; i4_1_1 < l4_1_1.size(); i4_1_1++) {
iterationContext.addContext(new IterationContext(l4_1_1.get(i4_1_1)));
MObject e4_1_1 = l4_1_1.get(i4_1_1);
m4_1_1_1(e4_1_1, i4_1_1, l4_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_1_1*/


/* CommaSeparatedListType - 4_1_1_1 */
private void m4_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_1 = new NodeInstance();
n4_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_1_1_1.setContext (activationContext);
n4_1_1_1.setParameter ("text", "");
n4_1_1_1.setParameter ("startSeparator", "Part de ");
n4_1_1_1.setParameter ("characterStyle", "Emphaseple");
n4_1_1_1.setParameter ("separator", ", ");
n4_1_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_1, elt, index, maxIndex, iterationContext);
m4_1_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_1_1_1*/


/* SmartNavigationType - 4_1_1_1_1 - DependsOn - ModelElement */
private void m4_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_1_1 = new NodeInstance();
n4_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_1_1_1_1.setContext (activationContext);
n4_1_1_1_1.setInputMetaclass(Dependency.class);
n4_1_1_1_1.setOutputMetaclass(ModelElement.class);
n4_1_1_1_1.setParameter ("sort", false);
n4_1_1_1_1.setParameter ("outputStereotype", "None");
n4_1_1_1_1.setParameter ("relation", "DependsOn");
n4_1_1_1_1.setParameter ("sequenceMode", true);
n4_1_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_1_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_1_1_1_1 = nb.navigate(n4_1_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_1_1_1_1);
for (int i4_1_1_1_1 = 0; i4_1_1_1_1 < l4_1_1_1_1.size(); i4_1_1_1_1++) {
iterationContext.addContext(new IterationContext(l4_1_1_1_1.get(i4_1_1_1_1)));
MObject e4_1_1_1_1 = l4_1_1_1_1.get(i4_1_1_1_1);
m4_1_1_1_1_1(e4_1_1_1_1, i4_1_1_1_1, l4_1_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_1_1_1_1*/


/* CharacterType - 4_1_1_1_1_1 */
private void m4_1_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_1_1_1_1_1 = new NodeInstance();
n4_1_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_1_1_1_1_1.setContext (activationContext);
n4_1_1_1_1_1.setParameter ("text", "$Name");
n4_1_1_1_1_1.setParameter ("characterStyle", "Accentuation");
IProductionBehavior pb = ((IProductionBehavior)n4_1_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_1_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_1_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_1_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_1_1_1_1_1*/


/* ParagraphType - 4_2 - derives from */
private void m4_2(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_2 = new NodeInstance();
n4_2.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n4_2.setContext (activationContext);
n4_2.setParameter ("text", "");
n4_2.setParameter ("paragraphStyle", "Texte");
n4_2.setParameter ("characterStyle", "None");
n4_2.setParameter ("removeEmptyParagraph", true);
IProductionBehavior pb = ((IProductionBehavior)n4_2.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_2, elt, index, maxIndex, iterationContext);
m4_2_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_2, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_2", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_2*/


/* SmartNavigationType - 4_2_1 - DependsOnDependency - derive */
private void m4_2_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_2_1 = new NodeInstance();
n4_2_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_2_1.setContext (activationContext);
n4_2_1.setInputMetaclass(Requirement.class);
n4_2_1.setOutputMetaclass(Dependency.class);
n4_2_1.setParameter ("sort", false);
n4_2_1.setParameter ("outputStereotype", "derive");
n4_2_1.setParameter ("relation", "DependsOnDependency");
n4_2_1.setParameter ("sequenceMode", true);
n4_2_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_2_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_2_1 = nb.navigate(n4_2_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_2_1);
for (int i4_2_1 = 0; i4_2_1 < l4_2_1.size(); i4_2_1++) {
iterationContext.addContext(new IterationContext(l4_2_1.get(i4_2_1)));
MObject e4_2_1 = l4_2_1.get(i4_2_1);
m4_2_1_1(e4_2_1, i4_2_1, l4_2_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_2_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_2_1*/


/* CommaSeparatedListType - 4_2_1_1 */
private void m4_2_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_2_1_1 = new NodeInstance();
n4_2_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_2_1_1.setContext (activationContext);
n4_2_1_1.setParameter ("text", "");
n4_2_1_1.setParameter ("startSeparator", "Dérive de ");
n4_2_1_1.setParameter ("characterStyle", "Emphaseple");
n4_2_1_1.setParameter ("separator", ", ");
n4_2_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_2_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_2_1_1, elt, index, maxIndex, iterationContext);
m4_2_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_2_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_2_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_2_1_1*/


/* SmartNavigationType - 4_2_1_1_1 - DependsOn - ModelElement */
private void m4_2_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_2_1_1_1 = new NodeInstance();
n4_2_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_2_1_1_1.setContext (activationContext);
n4_2_1_1_1.setInputMetaclass(Dependency.class);
n4_2_1_1_1.setOutputMetaclass(ModelElement.class);
n4_2_1_1_1.setParameter ("sort", false);
n4_2_1_1_1.setParameter ("outputStereotype", "None");
n4_2_1_1_1.setParameter ("relation", "DependsOn");
n4_2_1_1_1.setParameter ("sequenceMode", true);
n4_2_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_2_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_2_1_1_1 = nb.navigate(n4_2_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_2_1_1_1);
for (int i4_2_1_1_1 = 0; i4_2_1_1_1 < l4_2_1_1_1.size(); i4_2_1_1_1++) {
iterationContext.addContext(new IterationContext(l4_2_1_1_1.get(i4_2_1_1_1)));
MObject e4_2_1_1_1 = l4_2_1_1_1.get(i4_2_1_1_1);
m4_2_1_1_1_1(e4_2_1_1_1, i4_2_1_1_1, l4_2_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_2_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_2_1_1_1*/


/* CharacterType - 4_2_1_1_1_1 */
private void m4_2_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_2_1_1_1_1 = new NodeInstance();
n4_2_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_2_1_1_1_1.setContext (activationContext);
n4_2_1_1_1_1.setParameter ("text", "$Name");
n4_2_1_1_1_1.setParameter ("characterStyle", "Accentuation");
IProductionBehavior pb = ((IProductionBehavior)n4_2_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_2_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_2_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_2_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_2_1_1_1_1*/


/* ParagraphType - 4_3 - satisfied by */
private void m4_3(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_3 = new NodeInstance();
n4_3.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n4_3.setContext (activationContext);
n4_3.setParameter ("text", "");
n4_3.setParameter ("paragraphStyle", "Texte");
n4_3.setParameter ("characterStyle", "None");
n4_3.setParameter ("removeEmptyParagraph", true);
IProductionBehavior pb = ((IProductionBehavior)n4_3.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_3, elt, index, maxIndex, iterationContext);
m4_3_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_3, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_3", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_3*/


/* SmartNavigationType - 4_3_1 - ImpactedDependency - satisfy */
private void m4_3_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_3_1 = new NodeInstance();
n4_3_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_3_1.setContext (activationContext);
n4_3_1.setInputMetaclass(Requirement.class);
n4_3_1.setOutputMetaclass(Dependency.class);
n4_3_1.setParameter ("sort", false);
n4_3_1.setParameter ("outputStereotype", "satisfy");
n4_3_1.setParameter ("relation", "ImpactedDependency");
n4_3_1.setParameter ("sequenceMode", true);
n4_3_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_3_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_3_1 = nb.navigate(n4_3_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_3_1);
for (int i4_3_1 = 0; i4_3_1 < l4_3_1.size(); i4_3_1++) {
iterationContext.addContext(new IterationContext(l4_3_1.get(i4_3_1)));
MObject e4_3_1 = l4_3_1.get(i4_3_1);
m4_3_1_1(e4_3_1, i4_3_1, l4_3_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_3_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_3_1*/


/* CommaSeparatedListType - 4_3_1_1 */
private void m4_3_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_3_1_1 = new NodeInstance();
n4_3_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_3_1_1.setContext (activationContext);
n4_3_1_1.setParameter ("text", "");
n4_3_1_1.setParameter ("startSeparator", "Satisfait par ");
n4_3_1_1.setParameter ("characterStyle", "Emphaseple");
n4_3_1_1.setParameter ("separator", ", ");
n4_3_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_3_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_3_1_1, elt, index, maxIndex, iterationContext);
m4_3_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_3_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_3_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_3_1_1*/


/* SmartNavigationType - 4_3_1_1_1 - Impacted - ModelElement */
private void m4_3_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_3_1_1_1 = new NodeInstance();
n4_3_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_3_1_1_1.setContext (activationContext);
n4_3_1_1_1.setInputMetaclass(Dependency.class);
n4_3_1_1_1.setOutputMetaclass(ModelElement.class);
n4_3_1_1_1.setParameter ("sort", false);
n4_3_1_1_1.setParameter ("outputStereotype", "None");
n4_3_1_1_1.setParameter ("relation", "Impacted");
n4_3_1_1_1.setParameter ("sequenceMode", true);
n4_3_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_3_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_3_1_1_1 = nb.navigate(n4_3_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_3_1_1_1);
for (int i4_3_1_1_1 = 0; i4_3_1_1_1 < l4_3_1_1_1.size(); i4_3_1_1_1++) {
iterationContext.addContext(new IterationContext(l4_3_1_1_1.get(i4_3_1_1_1)));
MObject e4_3_1_1_1 = l4_3_1_1_1.get(i4_3_1_1_1);
m4_3_1_1_1_1(e4_3_1_1_1, i4_3_1_1_1, l4_3_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_3_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_3_1_1_1*/


/* CharacterType - 4_3_1_1_1_1 */
private void m4_3_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_3_1_1_1_1 = new NodeInstance();
n4_3_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_3_1_1_1_1.setContext (activationContext);
n4_3_1_1_1_1.setParameter ("text", "$Name");
n4_3_1_1_1_1.setParameter ("characterStyle", "Accentuation");
IProductionBehavior pb = ((IProductionBehavior)n4_3_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_3_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_3_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_3_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_3_1_1_1_1*/


/* ParagraphType - 4_4 - verified by */
private void m4_4(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_4 = new NodeInstance();
n4_4.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n4_4.setContext (activationContext);
n4_4.setParameter ("text", "");
n4_4.setParameter ("paragraphStyle", "Texte");
n4_4.setParameter ("characterStyle", "None");
n4_4.setParameter ("removeEmptyParagraph", true);
IProductionBehavior pb = ((IProductionBehavior)n4_4.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_4, elt, index, maxIndex, iterationContext);
m4_4_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_4, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_4", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_4*/


/* SmartNavigationType - 4_4_1 - ImpactedDependency - verify */
private void m4_4_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_4_1 = new NodeInstance();
n4_4_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_4_1.setContext (activationContext);
n4_4_1.setInputMetaclass(Requirement.class);
n4_4_1.setOutputMetaclass(Dependency.class);
n4_4_1.setParameter ("sort", false);
n4_4_1.setParameter ("outputStereotype", "verify");
n4_4_1.setParameter ("relation", "ImpactedDependency");
n4_4_1.setParameter ("sequenceMode", true);
n4_4_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_4_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_4_1 = nb.navigate(n4_4_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_4_1);
for (int i4_4_1 = 0; i4_4_1 < l4_4_1.size(); i4_4_1++) {
iterationContext.addContext(new IterationContext(l4_4_1.get(i4_4_1)));
MObject e4_4_1 = l4_4_1.get(i4_4_1);
m4_4_1_1(e4_4_1, i4_4_1, l4_4_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_4_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_4_1*/


/* CommaSeparatedListType - 4_4_1_1 */
private void m4_4_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_4_1_1 = new NodeInstance();
n4_4_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_4_1_1.setContext (activationContext);
n4_4_1_1.setParameter ("text", "");
n4_4_1_1.setParameter ("startSeparator", "Vérifié par ");
n4_4_1_1.setParameter ("characterStyle", "Emphaseple");
n4_4_1_1.setParameter ("separator", ", ");
n4_4_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_4_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_4_1_1, elt, index, maxIndex, iterationContext);
m4_4_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_4_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_4_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_4_1_1*/


/* SmartNavigationType - 4_4_1_1_1 - Impacted - ModelElement */
private void m4_4_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_4_1_1_1 = new NodeInstance();
n4_4_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_4_1_1_1.setContext (activationContext);
n4_4_1_1_1.setInputMetaclass(Dependency.class);
n4_4_1_1_1.setOutputMetaclass(ModelElement.class);
n4_4_1_1_1.setParameter ("sort", false);
n4_4_1_1_1.setParameter ("outputStereotype", "None");
n4_4_1_1_1.setParameter ("relation", "Impacted");
n4_4_1_1_1.setParameter ("sequenceMode", true);
n4_4_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_4_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_4_1_1_1 = nb.navigate(n4_4_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_4_1_1_1);
for (int i4_4_1_1_1 = 0; i4_4_1_1_1 < l4_4_1_1_1.size(); i4_4_1_1_1++) {
iterationContext.addContext(new IterationContext(l4_4_1_1_1.get(i4_4_1_1_1)));
MObject e4_4_1_1_1 = l4_4_1_1_1.get(i4_4_1_1_1);
m4_4_1_1_1_1(e4_4_1_1_1, i4_4_1_1_1, l4_4_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_4_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_4_1_1_1*/


/* CharacterType - 4_4_1_1_1_1 */
private void m4_4_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_4_1_1_1_1 = new NodeInstance();
n4_4_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_4_1_1_1_1.setContext (activationContext);
n4_4_1_1_1_1.setParameter ("text", "$Name");
n4_4_1_1_1_1.setParameter ("characterStyle", "Accentuation");
IProductionBehavior pb = ((IProductionBehavior)n4_4_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_4_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_4_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_4_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_4_1_1_1_1*/


/* ParagraphType - 4_5 - refines */
private void m4_5(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_5 = new NodeInstance();
n4_5.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.ParagraphNode.ParagraphType");
n4_5.setContext (activationContext);
n4_5.setParameter ("text", "");
n4_5.setParameter ("paragraphStyle", "Texte");
n4_5.setParameter ("characterStyle", "None");
n4_5.setParameter ("removeEmptyParagraph", true);
IProductionBehavior pb = ((IProductionBehavior)n4_5.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_5, elt, index, maxIndex, iterationContext);
m4_5_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_5, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_5", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_5*/


/* SmartNavigationType - 4_5_1 - DependsOnDependency - refine */
private void m4_5_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_5_1 = new NodeInstance();
n4_5_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_5_1.setContext (activationContext);
n4_5_1.setInputMetaclass(Requirement.class);
n4_5_1.setOutputMetaclass(Dependency.class);
n4_5_1.setParameter ("sort", false);
n4_5_1.setParameter ("outputStereotype", "refine");
n4_5_1.setParameter ("relation", "DependsOnDependency");
n4_5_1.setParameter ("sequenceMode", true);
n4_5_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_5_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_5_1 = nb.navigate(n4_5_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_5_1);
for (int i4_5_1 = 0; i4_5_1 < l4_5_1.size(); i4_5_1++) {
iterationContext.addContext(new IterationContext(l4_5_1.get(i4_5_1)));
MObject e4_5_1 = l4_5_1.get(i4_5_1);
m4_5_1_1(e4_5_1, i4_5_1, l4_5_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_5_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_5_1*/


/* CommaSeparatedListType - 4_5_1_1 */
private void m4_5_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_5_1_1 = new NodeInstance();
n4_5_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CommaSeparatedListNode.CommaSeparatedListType");
n4_5_1_1.setContext (activationContext);
n4_5_1_1.setParameter ("text", "");
n4_5_1_1.setParameter ("startSeparator", "Raffine ");
n4_5_1_1.setParameter ("characterStyle", "Emphaseple");
n4_5_1_1.setParameter ("separator", ", ");
n4_5_1_1.setParameter ("endSeparator", "");
IProductionBehavior pb = ((IProductionBehavior)n4_5_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_5_1_1, elt, index, maxIndex, iterationContext);
m4_5_1_1_1(elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_5_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_5_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_5_1_1*/


/* SmartNavigationType - 4_5_1_1_1 - DependsOn - ModelElement */
private void m4_5_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_5_1_1_1 = new NodeInstance();
n4_5_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.navigation.SmartNavigationNode.SmartNavigationType");
n4_5_1_1_1.setContext (activationContext);
n4_5_1_1_1.setInputMetaclass(Dependency.class);
n4_5_1_1_1.setOutputMetaclass(ModelElement.class);
n4_5_1_1_1.setParameter ("sort", false);
n4_5_1_1_1.setParameter ("outputStereotype", "None");
n4_5_1_1_1.setParameter ("relation", "DependsOn");
n4_5_1_1_1.setParameter ("sequenceMode", true);
n4_5_1_1_1.setParameter ("inputStereotype", "None");
INavigationBehavior nb = ((INavigationBehavior)n4_5_1_1_1.getNodeType ().getNodeBehavior ());
List <? extends MObject> l4_5_1_1_1 = nb.navigate(n4_5_1_1_1, elt, index, maxIndex, iterationContext);
filterNodoc(l4_5_1_1_1);
for (int i4_5_1_1_1 = 0; i4_5_1_1_1 < l4_5_1_1_1.size(); i4_5_1_1_1++) {
iterationContext.addContext(new IterationContext(l4_5_1_1_1.get(i4_5_1_1_1)));
MObject e4_5_1_1_1 = l4_5_1_1_1.get(i4_5_1_1_1);
m4_5_1_1_1_1(e4_5_1_1_1, i4_5_1_1_1, l4_5_1_1_1.size(), iterationContext);
iterationContext.removeContext();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_5_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_5_1_1_1*/


/* CharacterType - 4_5_1_1_1_1 */
private void m4_5_1_1_1_1(MObject elt, int index, int maxIndex, IterationContext iterationContext) throws TemplateNodeException {
try {
NodeInstance n4_5_1_1_1_1 = new NodeInstance();
n4_5_1_1_1_1.setNodeTypeClass ("com.modelio.module.documentpublisher.nodes.production.CharacterNode.CharacterType");
n4_5_1_1_1_1.setContext (activationContext);
n4_5_1_1_1_1.setParameter ("text", "$Name");
n4_5_1_1_1_1.setParameter ("characterStyle", "Accentuation");
IProductionBehavior pb = ((IProductionBehavior)n4_5_1_1_1_1.getNodeType ().getNodeBehavior ());
pb.beginProduction(n4_5_1_1_1_1, elt, index, maxIndex, iterationContext);
if (pb.endProduction(n4_5_1_1_1_1, iterationContext)) {
   this.activationContext.incrementProductionCount();
}
} catch (TemplateNodeException e) {
throw e;
} catch (Exception e) {
this.logger.error(e);
throw new TemplateNodeException("4_5_1_1_1_1", "TemplateExigences_1_0", e.getLocalizedMessage());
}
} /* END 4_5_1_1_1_1*/

}
