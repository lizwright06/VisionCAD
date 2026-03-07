//imports
import type { App } from "vue";
import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import type { ThemeDefinition } from "vuetify";
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'

export default (app: App) => {
    //themes
    const themes: Record<string, ThemeDefinition> = {
        light: {
            dark: false,
            colors: {
                //TODO: clean up palette & take out comments
                primary: '#A05DCB',           // Primary accent
                'primary-lighten-1': '#D0B4EF', // Light variant for hover / cards
                'primary-lighten-2': '#EAD9F9', // Very light background
                'primary-darken-1': '#8100B4',   // Dark variant for headers / text
                'primary-darken-2': '#57058B',   // Darkest / main background

                secondary: '#8A2FC9',         // Muted purple accent
                'secondary-lighten-1': '#9B3DDB', // Hover / active state
                'secondary-darken-1': '#6F0E96',   // Shadow / depth accent

                'on-primary': '#FFFFFF',       // Text on primary buttons
                'on-secondary': '#FFFFFF',     // Text on secondary buttons
                background: '#EAD9F9',       // Default light background
                surface: '#D0B4EF',          // Card / surface background
            },
            variables: {

            }
        }
    };

    //defaults
    const defaults = {
        VBtn: {
            color: "secondary",
            rounded: "lg",
            style: "text-transform: none; font-weight: 500;",
            variant: "flat"
        },
        VCard: {
            flat: true,
            rounded: "lg",
            border: false,
        },
        VAppBar: {
            color: "primary-darken-2",
            VBtn: {
                color: "secondary",
                rounded: "lg",
                style: "text-transform: none; font-weight: 500;",
                variant: "flat"
            }
        },
        VFooter: {
            color: "primary-darken-2",
            VBtn: {
                color: "secondary",
                rounded: "lg",
                style: "text-transform: none; font-weight: 500;",
                variant: "flat"
            }
        },
        VFileUpload: {
            color: "primary"
        }
    };

    //creation
    const vuetify = createVuetify({
        aliases,
        defaults,
        theme: {
            defaultTheme: 'light',
            themes,
        },
        icons: {
            defaultSet: "mdi",
            aliases,
            sets: {
                mdi,
            },
        },
    });

    app.use(vuetify);
}