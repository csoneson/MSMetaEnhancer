from matchms import utils


class Curator:
    """
    Curator makes sure that all data is curated before the actual annotation can proceed.
    Currently, fixing CAS numbers to correct format is supported.
    """
    def curate_spectra(self, spectra):
        """
        Iterates over given spectrums and curates individual spectra.

        :param spectra: given spectrums
        :return: curated spectrums
        """
        for spectrum in spectra.spectrums:
            spectrum.metadata = self.curate_metadata(spectrum.metadata)
        return spectra

    def curate_metadata(self, metadata):
        """
        Curate metadata of particular spectra.

        :param metadata: given metadata
        :return: curated metadata
        """
        if 'casno' in metadata:
            metadata['casno'] = self.fix_cas_number(metadata['casno'])
        return metadata

    @staticmethod
    def fix_cas_number(cas_number):
        """
        Adds dashes to CAS number.

        :param cas_number: given CAS number
        :return: CAS number enriched by dashes (if needed)
        """
        if "-" not in cas_number:
            return f'{cas_number[:-3]}-{cas_number[-3:-1]}-{cas_number[-1]}'
        return cas_number

    @staticmethod
    def filter_invalid_metadata(metadata):
        """
        Validates metadata and filters out invalid ones.

        :param metadata: metadata content
        :return: only valid metadata
        """
        filters = {
            'smiles': utils.is_valid_smiles,
            'inchi': utils.is_valid_inchi,
            'inchikey': utils.is_valid_inchikey
        }

        valid_metadata = {}
        for (attribute, value) in metadata.items():
            if attribute in filters.keys():
                if filters[attribute](value):
                    valid_metadata[attribute] = value
            else:
                valid_metadata[attribute] = value
        return valid_metadata
