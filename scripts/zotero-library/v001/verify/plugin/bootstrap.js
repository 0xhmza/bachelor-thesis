/* Throwaway test plugin: imports an RDF file into this (throwaway) profile, dumps the result, quits. */
var CONFIG = __CONFIG__;

async function startup({ id, version, rootURI }, reason) {
	try {
		await Zotero.initializationPromise;
		await Zotero.Schema.schemaUpdatePromise;
		const log = [];
		if (CONFIG.baseDir) {
			Zotero.Prefs.set('baseAttachmentPath', CONFIG.baseDir);
			Zotero.Prefs.set('saveRelativeAttachmentPath', true);
		}
		const file = Zotero.File.pathToFile(CONFIG.rdf);
		const translation = new Zotero.Translate.Import();
		translation.setLocation(file);
		const translators = await translation.getTranslators();
		log.push('translators: ' + translators.map(t => t.label + ' ' + t.translatorID).join(' | '));
		const rdfT = translators.find(t => t.translatorID === '5e3ad958-ac79-463d-812b-a86a9235c28f') || translators[0];
		translation.setTranslator(rdfT);
		const libraryID = Zotero.Libraries.userLibraryID;
		let err = null;
		try {
			await translation.translate({ libraryID, collections: null, linkFiles: CONFIG.linkFiles });
		}
		catch (e) { err = String(e) + '\n' + (e.stack || ''); }
		const items = await Zotero.Items.getAll(libraryID);
		const out = [];
		for (const item of items) {
			const j = item.toJSON();
			const rec = { key: item.key, type: item.itemType, json: j };
			if (item.isAttachment()) {
				rec.linkMode = item.attachmentLinkMode;
				rec.rawPath = item.attachmentPath;
				rec.filePath = await item.getFilePathAsync();
				rec.exists = rec.filePath ? await IOUtils.exists(rec.filePath) : false;
			}
			if (item.isNote()) rec.note = item.getNote();
			rec.parent = item.parentItemID ? Zotero.Items.get(item.parentItemID).key : null;
			out.push(rec);
		}
		await Zotero.File.putContentsAsync(CONFIG.out, JSON.stringify({ err, log, count: out.length, items: out, sortCheck: ['[40]', '[9]', '', '[100]', '[2]', '[17]', '[1]'].sort(Zotero.localeCompare) }, null, 1));
	}
	catch (e) {
		await Zotero.File.putContentsAsync(CONFIG.out, JSON.stringify({ fatal: String(e), stack: e.stack }));
	}
	Zotero.Utilities.Internal.quit();
}
function shutdown() {}
function install() {}
function uninstall() {}
